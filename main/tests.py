import json

from django.test import TestCase
from django.shortcuts import reverse

from main.forms import NewOrderForm
from main.infrastructure.models import ProductModel, OrderModel
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

    def test_contacts(self):
        response = self.client.get(reverse('main:contacts'))
        self.assertEquals(response.status_code, 200)
        context = response.context[1].dicts[3]
        self.assertIn('contacts', context.keys())


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


class TestAcceptOrderView(TestCase):

    def test_anonym(self):
        response = self.client.get(reverse('main:accept'))
        self.assertEquals(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_accept_order(self):
        user = UserFactory()
        self.client.force_login(user)
        session = self.client.session
        session['order_number'] = 111111
        session.save()
        response = self.client.get(reverse('main:accept'))
        self.assertEquals(response.status_code, 200)


class TestAcceptOrderDoneView(TestCase):

    @classmethod
    def setUpTestData(cls):
        ProductModel.objects.create(
            id=1,
            code='1111',
            name='Test Product',
            price=100
        )

    def test_anonym(self):
        self.client.logout()
        response = self.client.get(reverse('main:accept-done'))
        self.assertEquals(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_post(self):
        user = UserFactory()
        self.client.force_login(user)
        session = self.client.session
        session['order_number'] = 111111
        session.save()
        payload = {
            'order': {
                'phone_number': '+79999999999',
                'products': [{'id': 1, 'code': '1111', 'price': 100}]
            },
        }
        payload['order'] = json.dumps(payload['order'])
        response = self.client.post(reverse('main:accept-done'), payload)
        self.assertEquals(response.status_code, 200)
        order = OrderModel.objects.get(order_id=session['order_number'])
        self.assertTrue(order)
