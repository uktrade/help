import requests
from unittest import mock
from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse

from contact.generics.views import DITHelpView
from contact.generics.forms import DITHelpForm
from . import initial_data, response201, urls


@override_settings(ROOT_URLCONF=urls)
class TestGenericView(TestCase):

    @override_settings(ZENDESK_RESP_CODE=201, DEBUG=True)
    @mock.patch('requests.post')
    def test_zendesk_override_201(self, mock_post):
        """
        Setting a ZENDESK_RESP_CODE in the settings (usually done via environment variables), should mean that no post
        is submitted to zendesk, and the predetermined value of ZENDESK_RESP_CODE should be returned
        """

        # Setup the form with initial data
        form = DITHelpForm(initial_data, initial=initial_data)
        form.is_valid()

        # Post it to the generic view
        response = self.client.post(reverse('generic', kwargs={'service': 'test'}), form.cleaned_data)
        session = self.client.session

        # Make sure that requests.post was never called
        self.assertFalse(mock_post.called)

        # But the success data should have our 201 status code
        self.assertEquals(session['success_data']['code'], 201)

    @override_settings(ZENDESK_RESP_CODE=999, DEBUG=True)
    @mock.patch('requests.post')
    def test_zendesk_override_999(self, mock_post):
        """
        As above, but test that we get back the (non-existent) test response code we define
        """

        form = DITHelpForm(initial_data, initial=initial_data)
        form.is_valid()

        response = self.client.post(reverse('generic', kwargs={'service': 'test'}), form.cleaned_data)
        session = self.client.session

        # post still not called
        self.assertFalse(mock_post.called)

        # Test we get our 999 status code
        self.assertEquals(session['success_data']['code'], 999)

    @override_settings(ZENDESK_RESP_CODE=999, DEBUG=False)
    @mock.patch('requests.post', mock.MagicMock(return_value=response201))
    def test_zendesk_override_no_debug(self):
        """
        As above, but it should only NOT attempt to raise a ticket when DEBUG is True, so that it is impossible to
        accidentally bypass zendesk in production
        """

        form = DITHelpForm(initial_data, initial=initial_data)
        form.is_valid()

        response = self.client.post(reverse('generic', kwargs={'service': 'test'}), form.cleaned_data)
        session = self.client.session

        # post should now be called
        self.assertTrue(requests.post.called)

        # Test we get our 999 status code
        self.assertEquals(session['success_data']['code'], 201)

    @override_settings(ZENDESK_RESP_CODE=201, DEBUG=True)
    def test_return_link(self):
        """
        Test that when a form view receives an http referer, that referer is present on the success page
        as a return link
        """

        # Send the request with a referer
        referer = 'http://foo/bar'
        response = self.client.get(reverse('generic', kwargs={'service': 'test'}), HTTP_REFERER=referer)

        # Get the initial form data
        form = response.context_data['form']
        data = form.initial

        # Add the mandatory name and email data
        data['contact_name'] = initial_data['contact_name']
        data['contact_email'] = initial_data['contact_email']

        # Post it back, following the redirect
        response = self.client.post(reverse('generic', kwargs={'service': 'test'}), data, follow=True)
        link = '<a href="{0}" class="link" title="go back">< Go back</a>'.format(referer)

        # The reponse should contain a 'Go back' link to the referring page
        self.assertContains(response, link)

    @override_settings(ZENDESK_RESP_CODE=201, DEBUG=True)
    def test_no_return_link(self):
        """
        Test that when a form view receives an http referer, that referer is present on the success page
        as a return link
        """

        referer = 'http://foo/bar'

        # Send the request without a referer
        response = self.client.get(reverse('generic', kwargs={'service': 'test'}))

        # Get the initial form data
        form = response.context_data['form']
        data = form.initial

        # Add the mandatory name and email data
        data['contact_name'] = initial_data['contact_name']
        data['contact_email'] = initial_data['contact_email']

        # Post it back, following the redirect
        response = self.client.post(reverse('generic', kwargs={'service': 'test'}), data, follow=True)
        link = 'title="go back">< Go back</a>'

        # The response should have no 'Go back; link
        self.assertNotContains(response, link)


class TestFeedbackView(TestCase):

    def test_contact_get(self):
        response = self.client.get(reverse('contact:feedback_submit', kwargs={'service': 'test'}))
        self.assertContains(response, "Feedback", status_code=200)
        form = response.context_data['form']
        self.assertEquals(form['service'].value(), initial_data['service'])
