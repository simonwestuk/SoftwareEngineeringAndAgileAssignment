from django.contrib.auth import get_user_model, login
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from datetime import datetime

from django.urls import reverse

from user.models import User

# TODO: add comments of all the test cases you're NOT covering because django covers them for you


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='test_user',
            email="JDoe@email.com",
            password='asdfasdf123123'
        )
        self.user.save()
        self.client.force_login(self.user)
        self.another_user = User.objects.create(
            username='test_user2',
            email="JDoe2@email.com",
            password='asdfasdf123123'
        )
        self.another_user.save()

    # Create tests



    # Read tests



    # Update tests



    # Delete tests



