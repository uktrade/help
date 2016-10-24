import json
import requests

from django import forms
from django.conf import settings


class DITHelpForm(forms.Form):
    """
    This is a base form not inteded to be used directly, but inherited from, so that deriving forms can all easily
    submit tickets to Zendesk using a common method.
    """

    contact_name = forms.CharField(required=True, label="Name")
    contact_email = forms.EmailField(required=True, label="Email")
    originating_page = forms.CharField(required=False, widget=forms.HiddenInput())
    service = forms.CharField(required=True, widget=forms.HiddenInput())

    def get_body(self):
        origin_page = self.cleaned_data.get('originating_page')
        body = "User was on page:{0}".format(origin_page)
        return body

    def raise_zendesk_ticket(self):
        name = self.cleaned_data.get('contact_name')
        email = self.cleaned_data.get('contact_email')
        service = self.cleaned_data.get('service')
        body = self.get_body()

        # Form the data object
        data = {
            'ticket': {
                'subject': settings.ZENDESK_SUBJECT,
                'comment': {'body': body},
                'custom_fields': [{'id': 31281329, 'value': service}],
                'requester': {
                    'name': name,
                    "email": email
                }
            }
        }

        # Encode the data to create a JSON payload
        payload = json.dumps(data)

        # Set the request parameters
        user = "{0}/token".format(settings.ZENDESK_USER)
        pwd = settings.ZENDESK_TOKEN
        url = settings.ZENDESK_URL

        headers = {'content-type': 'application/json'}

        # Do the HTTP post request
        response = requests.post(url, data=payload, auth=(user, pwd), headers=headers)

        # Return True/False if a ticket was created (201), and the status code
        return response.status_code == 201, response.status_code


class FeedbackForm(DITHelpForm):
    content = forms.CharField(label="Feedback", required=True, widget=forms.Textarea)

    @property
    def get_form_name(self):
        return "Feedback"

    def get_body(self):
        content = self.cleaned_data.get('content')
        origin_page = self.cleaned_data.get('originating_page')
        if origin_page:
            content = self.cleaned_data.get('content')
            body = "User was on page:{0}\n\n{1}".format(origin_page, content)
        else:
            body = "{0}".format(content)
        return body
