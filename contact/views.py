from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

from .generics.views import DITHelpView, DITThanksView
from .forms import FeedbackForm, TriageForm


class InterstitialContactView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, service=None):
        # Get the HTTP_REFERER from the request and store it in the session for the DITHelpView
        originating_page = self.request.META.get('HTTP_REFERER')
        self.request.session['originating_page'] = originating_page

        # Perform the standard context processing
        return super().get_context_data(service=service)


class ThanksView(DITThanksView):
    """
    Default thanks page for the any form, no non-standard behaviour required.
    """
    pass


class FeedbackView(DITHelpView):
    """
    Standard basic Feedback view, use the default behaviour of the DITHelpView with the FeedbackForm
    """
    form_class = FeedbackForm
    form_title = "Feedback"
    success_url = reverse_lazy('contact:feedback_thanks')


class FeedbackThanksView(DITThanksView):
    """
    Thanks page for the FeedbackView, no non-standard behaviour required yet.
    """
    pass


class TriageView(DITHelpView):
    form_class = TriageForm
    form_title = "Contact an ecommerce adviser"
    template_name = "triage.html"
