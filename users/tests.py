from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LogoutViewTests(TestCase):
    def test_logout_redirects_to_dashboard_home(self):
        user = User.objects.create_user(username='alice', password='pass1234')
        self.client.force_login(user)

        response = self.client.post(reverse('users:logout'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:home'))
