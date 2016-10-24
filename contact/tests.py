from unittest import mock
from django.test import TestCase
from django.core.urlresolvers import reverse
from .forms import FeedbackForm
from .views import FeedbackView


initial_data = {
    'contact_name': 'Spam Eggs',
    'contact_email': 'spam@example.com',
    'content': 'testing contact form',
    'service': 'test'
}


class FeedbackFormTests(TestCase):

    def test_form_valid(self):
        form = FeedbackForm()
        self.assertFalse(form.is_valid())
        form = FeedbackForm(initial_data, initial=initial_data)
        self.assertTrue(form.is_valid())


class FeedbackView(TestCase):

    def test_contact_get(self):
        response = self.client.get(reverse('contact:feedback_submit', kwargs={'service': 'test'}))
        self.assertContains(response, "Feedback", status_code=200)
