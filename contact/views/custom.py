from ..generics.views import DITThanksView

from thumber.decorators import thumber_feedback


@thumber_feedback
class TriageThanks(DITThanksView):
    """
    Thanks page for the TriageView, just use the specific template, no other specific behaviour.
    """
    template_name = "soo/TriageForm/thanks.html"
    satisfied_wording = "We are sorry to hear that. Would you tell us why?"
