import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.settings import DEBUG
from logger import Logger
from main.application.services.commands.create_order import CreateOrder
from main.application.services.commands.get_order_numbers import GetOrderNumbers
from main.application.services.commands.send_email import SendEmailWithOrder
from main.application.services.services import CreateOrderService
from main.domain.entities import Product
from main.forms import NewOrderForm
from main.domain.aggregates import Order
from shared.infrastructure.uow import UnitOfWork, TestUnitOfWork


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
    uow = UnitOfWork() if not DEBUG else TestUnitOfWork()
    logger = Logger()
    get_order_numbers_command = GetOrderNumbers(logger)
    order_numbers = get_order_numbers_command(uow)

    def get(self, request, *args, **kwargs):
        try:
            order_number = str(Order.generate_order_number(self.order_numbers))
            request.session['order_number'] = order_number
            context = {
                'title': 'Оформление заказа',
                'order_number': order_number
            }
            return self.render_to_response(context)
        except Exception:
            self.logger.error(f'Ошибка на странице подтверждения заказа у пользователя: '
                              f'{self.request.user.email}')


class AcceptOrderDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'main/accept-done.html'
    extra_context = {'title': 'Оформление заказа'}
    send_email_with_order = SendEmailWithOrder()
    uow = UnitOfWork() if not DEBUG else TestUnitOfWork()
    logger = Logger()
    create_order_command = CreateOrder(logger)
    create_order_service = CreateOrderService(
        create_order_command, send_email_with_order, uow, logger
    )

    def post(self, request, **kwargs):
        try:
            order_number = request.session['order_number']
            order = json.loads(request.POST['order'])
            order = Order.factory(
                number=order_number,
                phone_number=order['phone_number'],
                email=self.request.user.email,
                user_id=self.request.user.pk,
                products=[
                    Product.factory(
                        _id=item['id'],
                        code=item['code'],
                        price=item['price']
                    ) for item in order['products']
                ],
            )
            self.create_order_service.execute(order)
            self.extra_context.update({
                'order_number': order_number,
                'email': self.request.user.email,
            })
            return super().render_to_response({})
        except Exception:
            self.logger.error(f'Ошибка на странице создания заказа у пользователя '
                              f'{self.request.user.email}')


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты'})


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
