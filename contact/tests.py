import requests
import json

from unittest import mock
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from .forms import FeedbackForm
from .views import FeedbackView


initial_data = {
    'contact_name': 'Spam Eggs',
    'contact_email': 'spam@example.com',
    'content': 'testing contact form',
    'service': 'test',
    'originating_page': 'google.com'
}

response201 = requests.Response()
response201.status_code = 201


class FeedbackView(TestCase):

    def test_contact_get(self):
        response = self.client.get(reverse('contact:feedback_submit', kwargs={'service': 'test'}))
        self.assertContains(response, "Feedback", status_code=200)
        form = response.context_data['form']
        self.assertEquals(form['service'].value(), initial_data['service'])


class FeedbackFormTests(TestCase):

    def test_form_valid(self):
        form = FeedbackForm()
        self.assertFalse(form.is_valid())
        form = FeedbackForm(initial_data, initial=initial_data)
        self.assertTrue(form.is_valid())

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
