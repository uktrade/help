from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.utils.http import urlquote

from .forms import DITHelpForm, FeedbackForm


class DITHelpView(FormView):
    template_name = 'help.html'
    form_class = DITHelpForm

    def form_valid(self, form):
        origin_page = form.cleaned_data.get('originating_page')
        success, code = form.raise_zendesk_ticket()
        redirect_url = "{0}?success={1}&code={2}&redirect={3}"
        return redirect(redirect_url.format(reverse('contact:thanks'), success, code, urlquote(origin_page)))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['originating_page'] = self.request.META.get('HTTP_REFERER')
        kwargs['initial']['service'] = self.request.resolver_match.kwargs['service']
        return kwargs


class FeedbackView(DITHelpView):
    form_class = FeedbackForm


class ThanksView(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'success': self.request.GET.get('success') == 'True',
            'code': int(self.request.GET.get('code')),
            'origin_page': self.request.GET.get('redirect'),
        }

        return context
