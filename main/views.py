from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms import NewOrderForm
from main.services import UtilsOrder
from main.models import Order
from app.celery import send_email


def index(request):
    return render(request, 'main/index.html', {'title': 'Telegram bots'})


def about(request):
    return render(request, 'main/about.html', {'title': 'О технологии'})


def prices(request):
    return render(request, 'main/prices.html', {'title': 'Цены'})


class NewOrderView(LoginRequiredMixin, FormView, UtilsOrder):
    form_class = NewOrderForm
    template_name = 'main/new-order.html'
    extra_context = {'title': 'Новый заказ'}

    def form_valid(self, form):
        order_list = self.get_order(form.cleaned_data)
        self.request.session['new_order'] = order_list
        return JsonResponse({'status': 'ok'}, status=200)

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)


class AcceptOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'main/accept.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_dict = self.request.session['new_order']
        order = Order(**order_dict)

        context.update(
            {
                'title': 'Оформление заказа',
                'new_order': order,
                'email': self.request.user.email
            }
        )
        return context


class AcceptOrderDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'main/accept-done.html'

    def post(self, request, **kwargs):
        context = dict(**request.POST)
        order_dict = self.request.session['new_order']
        order_dict['user'] = self.request.user
        order = Order(**order_dict)
        order.save()

        del order_dict['user']
        send_email.delay(self.request.user.email, order_dict)

        context.update(
            {
                'title': 'Оформление заказа',
                'order_number': order.order_id,
                'email': self.request.user.email
            }
        )
        return super().render_to_response(context)


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты'})


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
