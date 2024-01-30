from django.test import TestCase
from django.test.client import RequestFactory
from django.shortcuts import reverse
from django.contrib import auth

from main.forms import NewOrderForm
from users.factories import UserFactory
from users.forms import LoginForm, RegistrationForm, ProfileForm
from users.models import User


class TestAuth(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_registration(self):
        response = self.client.get(reverse('users:registration'))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegistrationForm)

        response = self.client.post(reverse('users:registration'), data={
            'username': 'example',
            'email': 'example@gmail.com',
            'password1': '123123ewqEWQ',
            'password2': '123123ewqEWQ'
        })
        self.assertEquals(response.status_code, 302)
        user = User.objects.filter(username='example').first()
        self.assertIsInstance(user, User)
        self.assertIn('sessionid', response.cookies.keys())

    def test_registration_error(self):
        response = self.client.post(reverse('users:registration'), data={
            'username': 'example',
            'email': 'example@gmail.com',
            'password1': '123123ewqEWQ',
            'password2': '123123ewqEW'
        })
        self.assertEquals(response.status_code, 200)
        error = response.context_data['form'].error_messages['password_mismatch']
        self.assertEquals(error, 'Введенные пароли не совпадают.')
        user = User.objects.filter(username='example').first()
        self.assertFalse(user)
        self.assertNotIn('sessionid', response.cookies.keys())

    def test_logout(self):
        User.objects.create_user(
            username='example', email='example@gmail.com', password='secret'
        )
        self.client.login(username='example', password='secret')
        self.assertTrue(self.client.cookies['sessionid'].value)
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.cookies['sessionid'].value)
