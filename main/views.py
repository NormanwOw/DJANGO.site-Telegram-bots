from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms import NewOrderForm
from main.utils import UtilsOrder
from main.models import Order


def index(request):
    return render(request, 'main/index.html', {'title': 'Telegram bots'})


def about(request):
    return render(request, 'main/about.html', {'title': 'О технологии'})


def prices(request):
    return render(request, 'main/prices.html', {'title': 'Цены'})


class NewOrder(FormView, LoginRequiredMixin, UtilsOrder):
    form_class = NewOrderForm
    template_name = 'main/new-order.html'
    success_url = reverse_lazy('main:accept')
    extra_context = {'title': 'Новый заказ'}

    def form_valid(self, form):
        order_list = self.get_order(form.cleaned_data)
        self.request.session['new_order'] = order_list

        return super().form_valid(form)


class AcceptOrder(TemplateView, LoginRequiredMixin):
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


class AcceptOrderDone(TemplateView, LoginRequiredMixin):
    template_name = 'main/accept-done.html'

    def post(self, request, **kwargs):
        context = dict(**request.POST)
        order_dict = self.request.session['new_order']
        order_dict['user'] = self.request.user
        order = Order(**order_dict)
        order.save()

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
    return render(request, 'page404.html')
