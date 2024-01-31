from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.http import urlencode

from users.forms import LoginForm, RegistrationForm, ProfileForm
from users.models import User
from main.models import Order


class TestAuth(TestCase):

    def setUp(self):
        self.password = 'secret'
        self.user = User.objects.create_user(
            username='example', email='example@gmail.com', password=self.password
        )

    def test_registration(self):
        response = self.client.get(reverse('users:registration'))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegistrationForm)

        response = self.client.post(reverse('users:registration'), data={
            'username': 'example2',
            'email': 'example2@gmail.com',
            'password1': '123123ewqEWQ',
            'password2': '123123ewqEWQ'
        })
        self.assertEquals(response.status_code, 302)
        user = User.objects.filter(username='example').first()
        self.assertIsInstance(user, User)
        self.assertIn('sessionid', response.cookies.keys())

    def test_registration_error(self):
        response = self.client.post(reverse('users:registration'), data={
            'username': 'example2',
            'email': 'example2@gmail.com',
            'password1': '123123ewqEWQ',
            'password2': '123123ewqEW'
        })
        self.assertEquals(response.status_code, 200)
        error = response.context_data['form'].error_messages['password_mismatch']
        self.assertEquals(error, 'Введенные пароли не совпадают.')
        user = User.objects.filter(username='example2').first()
        self.assertFalse(user)
        self.assertNotIn('sessionid', response.cookies.keys())

    def test_login(self):
        response = self.client.get(reverse('main:home'))
        self.assertNotIn('sessionid', response.cookies.keys())

        response = self.client.get(reverse('users:login'))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LoginForm)

        response = self.client.post(reverse('users:login'), data={
            'username': self.user.username,
            'password': self.password
        })
        self.assertEquals(response.status_code, 302)
        self.assertIn('sessionid', response.cookies.keys())

    def test_logout(self):
        self.client.login(username=self.user.username, password=self.password)
        self.assertTrue(self.client.cookies['sessionid'].value)

        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.cookies['sessionid'].value)

    def test_change_password_anonym(self):
        response = self.client.get(reverse('users:password-change'))
        self.assertEquals(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_change_password(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(reverse('users:password-change'))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PasswordChangeForm)

        response = self.client.post(reverse('users:password-change'), data={
            'old_password': self.password,
            'new_password1': 'secret123EWQ',
            'new_password2': 'secret123EWQ'
        })
        self.assertEquals(response.status_code, 302)
        self.assertIn('password-change/done', response.url)

        self.client.login(username=self.user.username, password='secret123EWQ')
        self.assertTrue(self.client.cookies['sessionid'].value)

    def test_change_password_error(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.post(reverse('users:password-change'), data={
            'old_password': 'secret2',
            'new_password1': 'secret123EWQ',
            'new_password2': 'secret123EWQ'
        })
        self.assertEquals(response.status_code, 200)
        error = response.context['form'].error_messages['password_incorrect']
        self.assertIn('Ваш старый пароль введен неправильно.', error)


class TestUserProfileView(TestCase):

    def setUp(self):
        self.password = 'secret'
        self.user = User.objects.create_user(
            username='example', email='example@gmail.com', password=self.password
        )
        self.order = 1111111
        Order.objects.create(
            order_id=self.order,
            user=self.user,
            phone_number='+79999999999',
            bot_shop=1000,
            admin_panel=1000,
            database=1000,
            total_price=3000
        )
        self.other_user = User.objects.create_user(
            username='other_user', email='other_user@gmail.com', password='secret'
        )
        self.other_order = 2222222
        Order.objects.create(
            order_id=self.other_order,
            user=self.other_user,
            phone_number='+79999999999',
            bot_shop=1000,
            admin_panel=1000,
            database=1000,
            total_price=3000
        )

    def test_profile_anonym(self):
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_profile(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ProfileForm)

    def test_profile_update_user(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.post(
            reverse('users:profile', kwargs={'pk': self.user.pk}), data={
                'first_name': 'name',
                'last_name': 'name',
                'email': 'example2@gmail.com'
            }
        )
        self.assertEquals(response.status_code, 302)
        user = User.objects.filter(first_name='name')
        self.assertTrue(user)

    def test_profile_update_user_error(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.post(
            reverse('users:profile', kwargs={'pk': self.user.pk}), data={
                'email': self.other_user.email
            })
        self.assertEquals(response.status_code, 200)
        error = response.context_data['form'].errors['email'].data[0].message
        self.assertEquals('Пользователь с таким Email уже существует.', error)

    def test_remove_order(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(
            reverse('users:profile', kwargs={'pk': self.user.pk}) + '?' +
            urlencode({'remove-order': self.order})
        )
        self.assertEquals(response.status_code, 200)
        order = Order.objects.filter(order_id=self.order)
        self.assertFalse(order)

    def test_remove_order_error(self):
        """Try to remove other order"""

        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(
            reverse('users:profile', kwargs={'pk': self.user.pk}) + '?' +
            urlencode({'remove-order': self.other_order})
        )
        self.assertEquals(response.status_code, 404)
        order = Order.objects.filter(order_id=self.other_order)
        self.assertTrue(order)

    def test_profile_remove_user_error(self):
        """Try to remove other user"""

        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(
            reverse('users:profile', kwargs={'pk': self.other_user.pk}) + '?' +
            urlencode({'remove-user': True})
        )
        self.assertEquals(response.status_code, 404)
        user = User.objects.filter(pk=self.other_user.pk)
        self.assertTrue(user)

    def test_profile_remove_user(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(
            reverse('users:profile', kwargs={'pk': self.user.pk}) + '?' +
            urlencode({'remove-user': True})
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals('/', response.url)

        user = User.objects.filter(pk=self.user.pk)
        self.assertFalse(user)

        User.objects.create_user(
            username=self.user.username,
            email=self.user.email,
            password=self.password
        )
