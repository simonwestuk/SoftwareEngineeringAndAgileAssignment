from django.contrib.auth import get_user_model, login
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from datetime import datetime

from django.urls import reverse

from .models import User

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

    def test_that_first_name_cannot_have_numbers(self):
        self.user.first_name = '1'

        with self.assertRaises(ValidationError):
            self.user.full_clean()

        self.user.first_name = '1a'

        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_that_last_name_cannot_have_numbers(self):
        self.user.last_name = '1'

        with self.assertRaises(ValidationError):
            self.user.full_clean()

        self.user.last_name = '1a'

        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_that_an_authenticated_user_can_see_the_update_view_for_himself(self):
        response = self.client.get(reverse('user:update_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200) # due to the redirect defined by success_url
        self.assertTemplateUsed(response, 'user/update_user_form.html')

    def test_that_an_authenticated_user_cannot_see_the_update_view_for_another_user(self):

        response = self.client.get(reverse('user:update_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_see_the_update_view_for_another_user(self):
        self.client.logout()
        response = self.client.get(reverse('user:update_user', args=[1]), follow=True)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_that_an_authenticated_user_can_see_the_delete_confirmation_for_himself(self):
        response = self.client.get(reverse('user:delete_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200) # due to the redirect defined by success_url
        self.assertTemplateUsed(response, 'user/user_confirm_delete.html')

    def test_that_an_authenticated_user_can_delete_his_own_account(self):
        response = self.client.post(reverse('user:delete_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_that_an_authenticated_user_cannot_see_the_delete_confirmation_for_another(self):
        response = self.client.get(reverse('user:delete_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403) # due to the redirect defined by success_url
        self.assertTemplateNotUsed(response, 'user/user_confirm_delete.html')