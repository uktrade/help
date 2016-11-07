from django.core.urlresolvers import reverse_lazy

from .generics.views import DITHelpView, DITThanksView
from .forms import FeedbackForm, TriageForm


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
    form_title = "Enquiry form"
    form_description = "Help with preferential rates"
    template_name = "triage.html"
