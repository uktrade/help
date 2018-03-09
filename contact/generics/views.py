import os
import requests

from importlib import import_module
from urllib.parse import urlparse

from django.conf import settings
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy, resolve
from django.http import Http404

from thumber import thumber_feedback

DIRECT_REQUEST = "Direct request"


class DITHelpView(FormView):
    """
    A base FormView that works with a subclass of the DITHelpForm.  It handles setting the initial data for the form,
    instructing the form to submit a ticket to zendesk, and storing success data in the session for use in the success
    page.  Unless overriden, the success view is the DITThanksView below.

    This view will automatically dispatch to a form class that is named in the URL, and handle a lot of 'magic' for
    you, but you can also subclass this View to add/modify any functionality you need.
    """

    def dispatch(self, *pargs, **kwargs):
        if self.form_class is None:
            try:
                self.form_name = self.request.resolver_match.kwargs['form_name']
                forms_module = import_module('contact.forms')
                self.form_class = getattr(forms_module, self.form_name)
            except KeyError:
                msg = 'You must specify a form_class attribute on the view, or have it as a parameter in the URL route'
                raise NotImplementedError(msg)
            except AttributeError:
                raise Http404
        else:
            self.form_name = self.form_class.__name__

        self.service = self.request.resolver_match.kwargs['service']

        return super().dispatch(*pargs, **kwargs)

    def get_success_url(self):
        if self.success_url is not None:
            return self.success_url

        return reverse_lazy('contact:generic_thanks', kwargs={'service': self.service, 'form_name': self.form_name})

    def get_template_names(self):
        if self.template_name is not None:
            return [self.template_name]

        specific_template = os.path.join(self.service, self.form_name, 'form.html')
        service_default_template = os.path.join(self.service, 'default_form.html')
        default_template = 'default_form.html'

        return [specific_template, service_default_template, default_template]

    def form_valid(self, form):
        """
        The submitted form is valid, so tell the form to raise a Zendesk ticket
        """
        # Get the originating page, and submit the ticket
        originating_page = form.cleaned_data.get('originating_page')

        override_resp_code = settings.ZENDESK_RESP_CODE
        if override_resp_code is not None and settings.DEBUG:
            resp_code = override_resp_code
        else:
            resp_code = form.raise_zendesk_ticket()

        if getattr(form, "save", False) and callable(getattr(form, "save")):
            form.save()

        # Story the above data in the session for (potential) use in the resulting view
        self.request.session['success_data'] = {
            'originating_page': originating_page,
            'valid_url': originating_page != DIRECT_REQUEST,
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
        kwargs['initial']['service'] = self.service
        return kwargs

    def get_form(self):
        """
        Set the request on the form, so that the form can use request params etc to modify it's behaviour
        """
        form = super().get_form()
        form.request = self.request
        return form

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

        originating_page = context['form']['originating_page'].value()
        if originating_page is not DIRECT_REQUEST:
            context['originating_page'] = originating_page

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
                    originating_page = DIRECT_REQUEST
            else:
                # The referer was from outside, so take it as the originating page
                originating_page = http_referer
        else:
            # The referer was blank, so must have been a direct request
            originating_page = DIRECT_REQUEST

        return originating_page

    def get_form_title(self):
        """
        Placeholder that can be overriden in an inheriting view
        """
        raise NotImplementedError()

    @property
    def form_title(self):
        """
        A property that returns self.get_form_title just as an easy accessor
        """
        return self.get_form_title()

    def get_form_subtitle(self):
        """
        Placeholder that can be overriden in an inheriting view
        """
        raise NotImplementedError()

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
    """

    def get_template_names(self):
        # If the inheriting class specifies a template, use that
        if self.template_name is not None:
            return [self.template_name]

        # No specific template given, so calculate potential template name options based on the service and form
        try:
            self.form_name = self.request.resolver_match.kwargs['form_name']
            self.service = self.request.resolver_match.kwargs['service']
        except AttributeError:
            raise Http404

        specific_template = os.path.join(self.service, self.form_name, 'thanks.html')
        service_default_template = os.path.join(self.service, 'default_thanks.html')
        default_template = 'default_thanks.html'

        return [specific_template, service_default_template, default_template]

    def get_context_data(self, *args, **kwargs):
        # Add the success_data that should be in the session
        context = super().get_context_data(*args, **kwargs)
        try:
            context['success_data'] = self.request.session['success_data']
        except IndexError:
            context['success_data'] = {'success': True}

        return context
