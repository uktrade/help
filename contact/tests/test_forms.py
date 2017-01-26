import requests
import json

from unittest import mock
from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse
from django.conf import settings

from . import initial_data, response201
from ..forms import FeedbackForm
from ..models import FeedbackModel


class FeedbackFormTests(TestCase):

    def test_form_valid(self):
        form = FeedbackForm()
        self.assertFalse(form.is_valid())
        form = FeedbackForm(initial_data, initial=initial_data)
        self.assertTrue(form.is_valid())

    @override_settings(USE_CAPTCHA=True)
    def test_captcha(self):
        form = FeedbackForm()
        self.assertFalse(form.is_valid())
        form = FeedbackForm(initial_data, initial=initial_data)
        self.assertFalse(form.is_valid())

    @mock.patch('requests.post', mock.Mock(return_value=response201))
    def test_form_zendesk_ticket_creation(self):
        # Setup the form with initial data, and validate it (to make sure form.cleaned_data is ready)
        form = FeedbackForm(initial_data, initial=initial_data)
        form.is_valid()

        # Tell the form to raise a ticket
        resp_code = form.raise_zendesk_ticket()

        # Make sure we get our 201 status code
        self.assertEquals(resp_code, response201.status_code)

        # Get the args and kwargs that the mock was called with
        mock_call_args = requests.post.call_args[0]
        mock_call_kwargs = requests.post.call_args[1]

        # Make sure the correct URL was used
        self.assertEquals(mock_call_args[0], settings.ZENDESK_URL)

        # Get the sent data to inspect
        data = json.loads(mock_call_kwargs['data'])
        ticket = data['ticket']

        # Check the body contains the content of the form, AND the originating page
        self.assertIn(initial_data['content'], ticket['comment']['body'])
        self.assertIn(initial_data['originating_page'], ticket['comment']['body'])

        # Check the forms contact email and name are in the requester field
        self.assertEquals(ticket['requester']['email'], initial_data['contact_email'])
        self.assertEquals(ticket['requester']['name'], initial_data['contact_name'])

        # Check the prescence of a hard coded pre-known custom field with ID and the service value
        self.assertEquals(len(ticket['custom_fields']), 1)
        self.assertEquals(ticket['custom_fields'][0]['id'], 31281329)
        self.assertEquals(ticket['custom_fields'][0]['value'], initial_data['service'])

    @override_settings(ZENDESK_RESP_CODE=201, DEBUG=True)
    def test_form_model_creation(self):
        # Make sure there is no feedback data stored
        self.assertEquals(FeedbackModel.objects.count(), 0)

        # Setup the form with initial data
        form = FeedbackForm(initial_data, initial=initial_data)
        form.is_valid()

        # Post it to the generic view
        url = reverse('contact:generic_submit', kwargs={'service': 'test', 'form_name': 'FeedbackForm'})
        response = self.client.post(url, form.cleaned_data)

        # We shoudl now have feedback data
        feedback = FeedbackModel.objects.all()
        self.assertEquals(len(feedback), 1)

        fb = feedback[0]
        self.assertEquals(fb.contact_name, initial_data['contact_name'])
        self.assertEquals(fb.contact_email, initial_data['contact_email'])
        self.assertEquals(fb.service, initial_data['service'])
        self.assertEquals(fb.originating_page, initial_data['originating_page'])
        self.assertEquals(fb.content, initial_data['content'])
