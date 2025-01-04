import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.application.services.commands.create_order import CreateOrder
from main.application.services.commands.get_order_numbers import GetOrderNumbers
from main.domain.entities import Product
from main.forms import NewOrderForm
from main.domain.aggregates import Order
from shared.infrastructure.uow import UnitOfWork


def index(request):
    return render(request, 'main/index.html', {'title': 'Telegram bots'})


def about(request):
    return render(request, 'main/about.html', {'title': 'О технологии'})


def prices(request):
    return render(request, 'main/prices.html', {'title': 'Цены'})


class NewOrderView(LoginRequiredMixin, FormView):
    form_class = NewOrderForm
    template_name = 'main/new-order.html'
    extra_context = {'title': 'Новый заказ'}

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)


class AcceptOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'main/accept.html'
    uow = UnitOfWork()
    get_order_numbers_command = GetOrderNumbers()
    order_numbers = get_order_numbers_command(uow)
    order_number = str(Order.generate_order_number(order_numbers))
    extra_context = {
        'title': 'Оформление заказа',
        'order_number': order_number
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        request.session['order_number'] = self.order_number
        return self.render_to_response(context)


class AcceptOrderDoneView(TemplateView, LoginRequiredMixin):
    template_name = 'main/accept-done.html'
    extra_context = {'title': 'Оформление заказа'}
    create_order_command = CreateOrder()
    uow = UnitOfWork()

    def post(self, request, **kwargs):
        order_number = request.session['order_number']
        order = json.loads(request.POST['order'])
        order = Order.factory(
            number=order_number,
            phone_number=order['phone_number'],
            user_id=self.request.user.pk,
            products=[
                Product.factory(
                    _id=item['id'],
                    code=item['code'],
                    price=item['price']
                ) for item in order['products']
            ],
        )
        self.create_order_command(self.uow, order)
        self.extra_context.update({
            'order_number': order_number,
            'email': self.request.user.email,
        })
        return super().render_to_response({})


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты'})


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
