import requests
from unittest import mock
from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse

from contact.generics.views import DITHelpView
from contact.generics.forms import DITHelpForm
from . import initial_data, response201, response200, response400


class TestGenericView(TestCase):

    @override_settings(ZENDESK_RESP_CODE=201, DEBUG=True)
    @mock.patch('requests.post')
    def test_incorrect_data_form(self, mock_post):
        invalid_form_data = {
            'company_name': 'ACME',
            'company_number': '12345678',
            'company_postcode': 'B12 G89',
            'contact_email': 'foo@bar.com',
            'contact_name': 'foo bar',
            'contact_phone': '123456789',
            'description': 'test',
            'experience': 'Yes, sometimes',
            'originating_page': 'Direct request',
            'service': 'test',
            'sku_count': 123,
            'trademarked': 'Yes',
            'turnover': '100k-500k',
            'validate': 'on',
            'website_address': 'dsadsadsa'
        }
        url = reverse('contact:generic_submit',
                      kwargs={'service': 'test', 'form_name': 'TriageForm'})
        response = self.client.post(url, invalid_form_data)
        assert mock_post.called is False
        assert response.context['form'].errors == {
            'website_address':
                ['Provide a link to where we can see your products online']
        }

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
        url = reverse('contact:generic_submit', kwargs={'service': 'test', 'form_name': 'DITHelpForm'})
        response = self.client.post(url, form.cleaned_data)
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

        url = reverse('contact:generic_submit', kwargs={'service': 'test', 'form_name': 'DITHelpForm'})
        response = self.client.post(url, form.cleaned_data)
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

        url = reverse('contact:generic_submit', kwargs={'service': 'test', 'form_name': 'DITHelpForm'})
        response = self.client.post(url, form.cleaned_data)
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
        url = reverse('contact:generic_submit', kwargs={'service': 'test', 'form_name': 'DITHelpForm'})
        response = self.client.get(url, HTTP_REFERER=referer)

        # Get the initial form data
        form = response.context_data['form']
        data = form.initial

        # Add the mandatory name and email data
        data['contact_name'] = initial_data['contact_name']
        data['contact_email'] = initial_data['contact_email']

        # Post it back, following the redirect
        response = self.client.post(url, data, follow=True)
        link = '<p><a href="{0}" class="link" title="go back">Go back to the previous page</a>.</p>'.format(referer)

        # The reponse should contain a 'Go back' link to the referring page
        self.assertContains(response, link)

    @override_settings(ZENDESK_RESP_CODE=201, DEBUG=True)
    def test_no_return_link(self):
        """
        Test that when a form view receives an http referer, that referer is present on the success page
        as a return link
        """

        referer = 'http://foo/bar'
        url = reverse('contact:generic_submit', kwargs={'service': 'test', 'form_name': 'DITHelpForm'})

        # Send the request without a referer
        response = self.client.get(url)

        # Get the initial form data
        form = response.context_data['form']
        data = form.initial

        # Add the mandatory name and email data
        data['contact_name'] = initial_data['contact_name']
        data['contact_email'] = initial_data['contact_email']

        # Post it back, following the redirect
        response = self.client.post(url, data, follow=True)
        link = 'title="go back">< Go back</a>'

        # The response should have no 'Go back; link
        self.assertNotContains(response, link)


class TestOtherViews(TestCase):

    @mock.patch('requests.get', mock.MagicMock(return_value=response200))
    def test_pingdom_200(self):
        response = self.client.get(reverse('contact:ping'))
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertIn('zendesk_resp_code', data)
        self.assertIn('info', data)
        self.assertEquals(200, data['zendesk_resp_code'])
        self.assertEquals('Success', data['info'])

    @mock.patch('requests.get', mock.MagicMock(return_value=response400))
    def _test_pingdom_400(self):
        """ Test deactivated for now """

        response = self.client.get(reverse('contact:ping'))
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertIn('zendesk_resp_code', data)
        self.assertIn('info', data)
        # Any non 200 response results in a server error for the pingdom view
        self.assertEquals(500, data['zendesk_resp_code'])

    def test_feedback_redirect(self):
        response = self.client.get(reverse('contact:feedback_submit', kwargs={'service': 'test'}), follow=True)
        self.assertContains(response, "Feedback", status_code=200)
        form = response.context_data['form']
        self.assertEquals(form['service'].value(), initial_data['service'])

    def test_triage_redirect(self):
        url = reverse('contact:triage_submit', kwargs={'service': 'test'})
        response = self.client.get("{0}?market=Foo".format(url), follow=True)
        self.assertContains(response, "Foo", status_code=200)
        form = response.context_data['form']
        self.assertEquals(form['service'].value(), initial_data['service'])
