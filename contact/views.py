from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.utils.http import urlquote

from .forms import FeedbackForm


class DITHelpViewMixin():
    """
    A mixin that handles populating a subclass of DITHelpForm, setting the initial data for the form, instructing the
    form to submit a ticket to zendesk, and storing success data in the session for use in the default success page.

    The minimum to make this mixin work, is to include it in a view that also inherits from FormView, and then set the
    form_class to a form that itself inherits from DITHelpForm.
    """

    template_name = 'help.html'
    success_url = reverse_lazy('contact:thanks')

    def form_valid(self, form):
        originating_page = form.cleaned_data.get('originating_page')
        success, code = form.raise_zendesk_ticket()
        self.request.session['success_data'] = {
            'originating_page': originating_page,
            'success': success,
            'code': code
        }
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['originating_page'] = self.request.META.get('HTTP_REFERER')
        kwargs['initial']['service'] = self.request.resolver_match.kwargs['service']
        return kwargs


class ThanksView(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, *args, **kwargs):
        context = {'success_data': self.request.session['success_data']}
        return context


class FeedbackView(DITHelpViewMixin, FormView):
    form_class = FeedbackForm
