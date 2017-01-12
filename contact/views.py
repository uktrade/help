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
    Default thanks page for any form, no non-standard behaviour required.
    """
    pass


class FeedbackView(DITHelpView):
    """
    Standard basic Feedback view, use the default behaviour of the DITHelpView with the FeedbackForm
    """
    form_class = FeedbackForm


class TriageView(DITHelpView):
    """
    Triage form view, for handling enquiries from users wanting to obtain the DIT negotiated terms with the online
    marketplaces.
    """
    form_class = TriageForm
    template_name = "triage.html"
    success_url = reverse_lazy('contact:triage_thanks')


class TriageThanksView(DITThanksView):
    """
    Thanks page for the TriageView, just use the specific template, no other specific behaviour.
    """
    template_name = "triage_thanks.html"
