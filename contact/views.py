import requests

from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.conf import settings

from thumber import thumber_feedback

from .generics.views import DITHelpView, DITThanksView
from .forms import FeedbackForm, TriageForm


class PingView(View):
    def get(self, request, *args, **kwargs):
        # Set the request parameters
        user = "{0}/token".format(settings.ZENDESK_USER)
        pwd = settings.ZENDESK_TOKEN
        url = settings.ZENDESK_TEST_URL
        headers = {'content-type': 'application/json'}

        # Do the HTTP post request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        if response.status_code != 200:
            status = 500
            info = response.json()['error']
        else:
            status = 200
            info = 'Success'

        return JsonResponse({
            'zendesk_resp_code': response.status_code,
            'info': info
        }, status=status)


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
    success_url = reverse_lazy('contact:triage_thanks')
    template_name = "triage.html"

    def get_form_title(self):
        market = self.request.GET.get('market', None)
        if market is not None:
            return market

        return None


@thumber_feedback
class TriageThanksView(DITThanksView):
    """
    Thanks page for the TriageView, just use the specific template, no other specific behaviour.
    """
    template_name = "triage_thanks.html"
