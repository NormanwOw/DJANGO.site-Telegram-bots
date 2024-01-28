from django.test import TestCase
from django.shortcuts import reverse

from main.forms import NewOrderForm
from users.factories import UserFactory


class TestMain(TestCase):

    def test_index(self):
        response = self.client.get(reverse('main:home'))
        self.assertEquals(response.status_code, 200)
        template = response.templates[1]
        tags = template.origin.loader.engine.template_libraries['main_tags'].tags
        response_menu = tags['menu']
        self.assertTrue(response_menu)
        contacts = tags['contact_list']
        self.assertTrue(contacts)

    def test_about(self):
        response = self.client.get(reverse('main:about'))
        self.assertEquals(response.status_code, 200)

    def test_prices(self):
        response = self.client.get(reverse('main:prices'))
        self.assertEquals(response.status_code, 200)
        template = response.templates[1]
        tags = template.origin.loader.engine.template_libraries['main_tags'].tags
        products = tags['product_list']
        self.assertTrue(products)


class TestNewOrderView(TestCase):

    def test_anonym(self):
        response = self.client.get(reverse('main:new-order'))
        self.assertEquals(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_new_order(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('main:new-order'))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], NewOrderForm)

        payload = {
            'phone_number': '+79999999999',
            'bot_shop': True,
            'admin_panel': True,
            'database': True,
        }

        response = self.client.post(reverse('main:new-order'), data=payload)
        self.assertEquals(response.status_code, 302)
        self.assertIn('accept', response.url)

        payload = {
            'phone_number': '+7999999',
            'bot_shop': True,
            'admin_panel': True,
            'database': True,
        }

        response = self.client.post(reverse('main:new-order'), data=payload)
        self.assertEquals(response.status_code, 200)
        errors = response.context[3].dicts[1]['errors']
        self.assertIn('Введите корректный номер телефона', errors)


class TestAcceptOrderView(TestCase):

    def test_anonym(self):
        response = self.client.get(reverse('main:accept'))
        self.assertEquals(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_accept_order(self):
        user = UserFactory()
        self.client.force_login(user)
        order = {
            'admin_panel': True,
            'bot_shop': True,
            'database': True,
            'order_id': '4444444',
            'phone_number': '+79999999999',
            'total_price': 0
        }
        session = self.client.session
        session['new_order'] = order
        session.save()
        response = self.client.get(reverse('main:accept'))
        self.assertEquals(response.status_code, 200)

