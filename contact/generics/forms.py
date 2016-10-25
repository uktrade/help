import json
import requests

from django import forms
from django.conf import settings


class DITHelpForm(forms.Form):
    """
    This is a base form not inteded to be used directly, but inherited from, so that deriving forms can all easily
    submit tickets to Zendesk using a common method.

    Due to the way that Django forms use metaclasses to configure the class, this cannot be an abstract base class.
    """

    contact_name = forms.CharField(required=True, label="Name")
    contact_email = forms.EmailField(required=True, label="Email")
    originating_page = forms.CharField(required=False, widget=forms.HiddenInput())
    service = forms.CharField(required=True, widget=forms.HiddenInput())

    def get_body(self):
        """
        An unimplemented function that needs to be overridden in the inheriting class.
        It should return the body of the Zendesk ticket to be raised, from fields on the inheriting form.
        """
        raise NotImplementedError('You need to implement the get_body in the inheriting form')

    def raise_zendesk_ticket(self):
        # Get some basic form values
        name = self.cleaned_data.get('contact_name')
        email = self.cleaned_data.get('contact_email')
        service = self.cleaned_data.get('service')

        # Construct the body of the message
        body = self.get_body()

        # Form the data object
        data = {
            'ticket': {
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

        # Return and the response status code
        return response.status_code
