from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy


class DITHelpView(FormView):
    """
    A base FormView that works with a subclass of the DITHelpForm.  It handles setting the initial data for the form,
    instructing the form to submit a ticket to zendesk, and storing success data in the session for use in the success
    page.  Unless overriden, the success view is the DITThanksView below.

    The minimum to make this mixin work, is to include it in a view that also inherits from FormView, and then set the
    form_class to a form that itself inherits from DITHelpForm.
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
        kwargs['initial']['originating_page'] = self.request.META.get('HTTP_REFERER')
        kwargs['initial']['service'] = self.request.resolver_match.kwargs['service']
        return kwargs


class DITThanksView(TemplateView):
    """
    A helper view for the success of a DITHelpView. Utilises the session data placed by the DITHelpView to render a
    useful Thanks page.

    NOTE: If used as a success page it needs success_data placed into the session, else an IndexError will result.
    """

    template_name = 'default_thanks.html'

    def get_context_data(self, *args, **kwargs):
        # Add the success_data that should be in the session
        context = super().get_context_data()
        context['success_data'] = self.request.session['success_data']
        return context
