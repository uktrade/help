import json
import requests

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import slugify

from raven.contrib.django.raven_compat.models import client


class DITHelpFormMetaclass(forms.Form.__class__):
    """
    Inherit the metaclass of the standard Form class to add some validation of the definition of the form itself.
    Make sure the definition of the form doesn't specify both a field_order AND and fieldsets attribute.
    """

    def __new__(mcs, *pargs, **kwargs):
        new_class = super(DITHelpFormMetaclass, mcs).__new__(mcs, *pargs, **kwargs)
        if new_class.field_order is not None and getattr(new_class, 'fieldsets', None) is not None:
            raise ImproperlyConfigured('Cannot specify both field_order and fieldsets on DITHelpForm')
        return new_class


class DITHelpForm(forms.Form, metaclass=DITHelpFormMetaclass):
    """
    This is a base form not inteded to be used directly, but inherited from, so that deriving forms can all easily
    submit tickets to Zendesk using a common method.

    Due to the way that Django forms use metaclasses to configure the class, this cannot be an abstract base class.
    """

    submit_text = "Submit"
    contact_name = forms.CharField(required=True, label="Name")
    contact_email = forms.EmailField(required=True, label="Email")
    originating_page = forms.CharField(required=False, widget=forms.HiddenInput())
    service = forms.CharField(required=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        """
        Get the data needed to test the Google recaptcha, and store it on the form object for the clean method
        """

        self._title = None

        self.captcha_response = kwargs.pop('captcha_response', None)
        self.remote_ip = kwargs.pop('remote_ip', None)
        super().__init__(*args, **kwargs)

        fieldsets = getattr(self, 'fieldsets', None)
        if fieldsets is not None:
            self.steps = []
            for step in fieldsets:
                fields = []
                for item in step[1]['fields']:
                    if isinstance(item, str):
                        fields.append([self[item]])
                    else:
                        fields.append([self[field_name] for field_name in item])

                self.steps.append({'title': step[0], 'slug': slugify(step[0]), 'fields': fields})

    def order_fields(self, field_order):
        fieldsets = getattr(self, 'fieldsets', None)
        if fieldsets is not None:
            field_order = []
            for step in fieldsets:
                field_order += step[1]['fields']

        return super().order_fields(field_order)

    def clean(self):
        """
        Validate the recaptcha by submitting the data to Google for verification
        """

        cleaned_data = super().clean()

        if settings.USE_CAPTCHA:
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {
                'secret': settings.CAPTCHA_SECRET_KEY,
                'response': self.captcha_response,
                'remoteip': self.remote_ip,
            }
            headers = {'content-type': 'application/json'}

            # Get the data for this form, and encode it to create a JSON payload
            payload = json.dumps(values)

            # Do the HTTP post request
            response = requests.post(url, data=payload, headers=headers)
            result = response.json()

            # result["success"] will be True on a success
            if not result["success"]:
                raise forms.ValidationError(u'Only humans are allowed to submit this form.')

        return cleaned_data

    def get_title(self):
        return self._title

    @property
    def title(self):
        """
        A property that returns self.get_title just as an easy accessor
        """
        return self.get_title()

    @title.setter
    def title(self, value):
        self._title = value

    def get_body(self):
        """
        Generate the body for a Zendesk ticket.  Loop over all fields adding the label and cleaned value to a string.
        Itended to be overwritten in the inheriting class to perform more specific behaviour, this should act as a
        sensible fallback
        """

        data_items = []
        for bound_field in self:
            data_items.append("{0}: \n{1}\n".format(bound_field.label, bound_field.value()))

        return "\n".join(data_items)

    def get_comment(self):
        """
        A method that returns the simplest comment body for the ticket creation request.
        Inheriting classes can implement this method (or the comment property) to provide custom comment data/structure

        See the Zendesk API docs for comment structure:
        https://developer.zendesk.com/rest_api/docs/core/ticket_comments
        """

        return {'body': self.body}

    def get_custom_fields(self):
        """
        A method that returns the custom fields for the ticket creation request.  It sets the service field in Zendesk
        to the one set in the form.
        Inheriting classes can implement this method (or the custom_fields property) to provide custom fields

        See the Zendesk API docs for custom fields:
        https://developer.zendesk.com/rest_api/docs/core/tickets#setting-custom-field-values
        """

        service = self.cleaned_data.get('service')
        custom_fields = [{'id': 31281329, 'value': service}]
        return custom_fields

    def get_requester(self):
        """
        A method that returns a simple requester body for the ticket creation request.
        Inheriting classes can implement this method (or the custom_fields property) to provide custom fields

        See the Zendesk API docs for requesters and sumitters:
        https://developer.zendesk.com/rest_api/docs/core/tickets#requesters-and-submitters
        """

        name = self.cleaned_data.get('contact_name')
        email = self.cleaned_data.get('contact_email')
        requester = {'name': name, 'email': email}
        return requester

    def get_ticket_data(self):
        """
        A method that returns the entire ticket data that will be sent to the Zendesk API.
        If extra fields (beyond comment, custom_fields, and requester) are required in the ticket creation, inheriting
        classes will need to override this method to add the extra properties.

        See the Zendesk API docs for the structure of the request data:
        https://developer.zendesk.com/rest_api/docs/core/tickets
        """

        data = {
            'ticket': {
                'comment': self.comment,
                'custom_fields': self.custom_fields,
                'requester': self.requester,
            }
        }

        return data

    @property
    def body(self):
        """
        Accessor for the get_body method, inheriting classes can either implement a get_body method, or set a
        non-dynamic body property
        """

        return self.get_body()

    @property
    def comment(self):
        """
        Accessor for the get_comment method, inheriting classes can either implement a get_comment method, or set a
        non-dynamic body property
        """

        return self.get_comment()

    @property
    def custom_fields(self):
        """
        Accessor for the get_custom_fields method, inheriting classes can either implement a get_custom_fields method,
        or set a non-dynamic custom_fields property
        """

        return self.get_custom_fields()

    @property
    def requester(self):
        """
        Accessor for the get_requester method, inheriting classes can either implement a get_requester method, or set a
        non-dynamic requester property
        """

        return self.get_requester()

    @property
    def ticket_data(self):
        """
        Accessor for the get_requester method, inheriting classes can either implement a get_requester method, or set a
        non-dynamic requester property
        """

        return self.get_ticket_data()

    def raise_zendesk_ticket(self):
        # Set the request parameters
        user = "{0}/token".format(settings.ZENDESK_USER)
        pwd = settings.ZENDESK_TOKEN
        url = settings.ZENDESK_URL

        headers = {'content-type': 'application/json'}

        # Get the data for this form, and encode it to create a JSON payload
        payload = json.dumps(self.get_ticket_data())

        # Do the HTTP post request
        response = requests.post(url, data=payload, auth=(user, pwd), headers=headers)

        if response.status_code != 201:
            client.capture('raven.events.Message',
                           message='Zendesk submission error',
                           data={},
                           extra={
                               'body': self.ticket_data,
                               'response_code': response.status_code,
                               'response_reason': response.reason
                           })

        # Return and the response status code
        return response.status_code
