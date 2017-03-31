from django.test import TestCase
from django.core.urlresolvers import reverse

from . import initial_data


class FeedbackView(TestCase):

    def test_contact_get(self):
        response = self.client.get(reverse('contact:feedback_submit', kwargs={'service': 'test'}))
        self.assertContains(response, "Feedback", status_code=200)
        form = response.context_data['form']
        self.assertEquals(form['service'].value(), initial_data['service'])
