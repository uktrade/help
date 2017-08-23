import requests

from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.conf import settings

from thumber.decorators import thumber_feedback

from ..generics.views import DITHelpView, DITThanksView


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
    template_name = 'landing.html'

    def get_context_data(self, service=None):
        # Get the HTTP_REFERER from the request and store it in the session for the DITHelpView
        originating_page = self.request.META.get('HTTP_REFERER')
        self.request.session['originating_page'] = originating_page

        # Perform the standard context processing
        return super().get_context_data(service=service)


class DefaultHelpView(DITHelpView):
    pass


@thumber_feedback
class DefaultThanksView(DITThanksView):
    pass
