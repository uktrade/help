import requests
from urllib.parse import urlparse

from django.conf import settings
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy, resolve


class DITHelpView(FormView):
    """
    A base FormView that works with a subclass of the DITHelpForm.  It handles setting the initial data for the form,
    instructing the form to submit a ticket to zendesk, and storing success data in the session for use in the success
    page.  Unless overriden, the success view is the DITThanksView below.

    To use this view correctly:
      * Create a view that inherits from this class
      * Add a 'form_class' property on the view definition to a form that itself inherits from DITHelpForm
      * Add a 'name' property, or a get_name method on the view definition that is the name/title of the form
        displayed in the template
      * Add any custom methods/properties that you need
    """

    template_name = 'default_form.html'
    success_url = reverse_lazy('contact:thanks')

    def form_valid(self, form):
        """
        The submitted form is valid, so tell the form to raise a Zendesk ticket
        """
        # Get the originating page, and submit the ticket
        originating_page = form.cleaned_data.get('originating_page')
        resp_code = form.raise_zendesk_ticket()

        # Story the above data in the session for (potential) use in the resulting view
        self.request.session['success_data'] = {
            'originating_page': originating_page,
            'success': resp_code == 201,
            'code': resp_code
        }

        # Perform the standrd form_valid method, which will redirect to the success page
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Get the form kwargs
        kwargs = super().get_form_kwargs()

        # Add the HTTP_REFERER, and service specified in the url, to the initial form data
        kwargs['initial']['originating_page'] = self._get_originating_page()
        kwargs['initial']['service'] = self.request.resolver_match.kwargs['service']
        kwargs['remote_ip'] = self.request.POST.get(u'g-recaptcha-response', None)
        kwargs['captcha_response'] = self.request.META.get("REMOTE_ADDR", None)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Try to get at title from the view, but don't worry if it's not implemented
        try:
            context['form'].title = self.form_title
        except NotImplementedError:
            pass

        # Try to get the subtitle from the view, but don't worry if it's not implemented
        try:
            context['form'].subtitle = self.form_subtitle
        except NotImplementedError:
            pass

        context['use_captcha'] = settings.USE_CAPTCHA
        context['captcha_site_key'] = settings.CAPTCHA_SITE_KEY

        return context

    def _get_originating_page(self):
        # Get the referer from the request, and parse it's data to find it's origin
        http_referer = self.request.META.get('HTTP_REFERER')
        if http_referer is not None:
            url_data = urlparse(http_referer)
            host = url_data.netloc
            path = url_data.path

            if host in settings.ALLOWED_HOSTS and resolve(path).view_name == 'contact:interstitial':
                # The referer is this app's intersitial view, so get the originating page from the session
                originating_page = self.request.session['originating_page']

                # If the value in the session was none, get it from the REFERER instead
                if originating_page is None:
                    originating_page = "Unknown"
            else:
                # The referer was from outside, so take it as the originating page
                originating_page = http_referer
        else:
            # The referer was blank, so must have been a direct request
            originating_page = "Direct request"

        return originating_page

    def get_form_title(self):
        msg = 'You must implement a get_form_title method or a form_title property in the inheriting view'
        raise NotImplementedError(msg)

    @property
    def form_title(self):
        """
        A property that returns self.get_form_title just as an easy accessor
        """
        return self.get_form_title()

    def get_form_subtitle(self):
        msg = 'You must implement a get_form_subtitle method or a form_subtitle property in the inheriting view'
        raise NotImplementedError(msg)

    @property
    def form_subtitle(self):
        """
        A property that returns self.get_form_subtitle just as an easy accessor
        """
        return self.get_form_subtitle()


class DITThanksView(TemplateView):
    """
    A helper view for the success of a DITHelpView. Utilises the session data placed by the DITHelpView to render a
    useful Thanks page.

    NOTE: If used as a success page it needs success_data placed into the session, else an IndexError will result.
    """

    template_name = 'default_thanks.html'

    def get_context_data(self, *args, **kwargs):
        # Add the success_data that should be in the session
        context = super().get_context_data(*args, **kwargs)
        context['success_data'] = self.request.session['success_data']
        return context
