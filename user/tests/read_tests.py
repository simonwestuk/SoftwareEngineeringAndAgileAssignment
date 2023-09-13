from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from user.models import User
from django.urls import reverse

from user.tests.test_utils import BaseTestCase


class ReadUserTestCase(BaseTestCase):

    def test_user_list_view(self):
        response = self.client.get(reverse('user:users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/users.html')

    def test_user_display_view(self):
        response = self.client.get(reverse('user:user', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user.html')