from django.test import TestCase
from django.urls import reverse


class AdminViewTests(TestCase):

    def test_admin_restricted(self):
        with self.settings(RESTRICT_ADMIN=True):
            response = self.client.get(reverse('admin:login'))
            assert response.status_code == 404

    def test_admin_unrestricted(self):
        with self.settings(RESTRICT_ADMIN=False):
            response = self.client.get(reverse('admin:login'))
            assert response.status_code == 200
