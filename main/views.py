from django.shortcuts import render
from django.forms.models import model_to_dict
import app.settings as settings

from main.models import Product, Order
from main.forms import NewOrderForm
from main.utils import UtilsOrder

menu = [{'name': 'О технологии', 'url': 'main:about'},
        {'name': 'Цены', 'url': 'main:prices'},
        {'name': 'Сделать заказ', 'url': 'main:new-order'},
        {'name': 'Контакты', 'url': 'main:contacts'}]

price_list = Product.objects.all()


def index(request):
    return render(request, 'main/index.html', {'title': 'Telegram bots', 'menu': menu})


def about(request):
    return render(request, 'main/about.html', {'title': 'О технологии', 'menu': menu})


def prices(request):
    context = {
        'title': 'Цены',
        'menu': menu,
        'price_list': price_list
    }
    return render(request, 'main/prices.html', context)


def new_order(request):
    form = NewOrderForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        order = UtilsOrder.get_order(form.cleaned_data)
        order_dict = model_to_dict(order, exclude=['date'])
        request.session.update({'order': order_dict})
        context = {
            'new_order': order,
            'menu': menu,
        }
        return render(request, 'main/accept.html', context)
    else:
        form = NewOrderForm()

    context = {
        'title': 'Новый заказ',
        'menu': menu,
        'price_list': price_list,
        'form': form
    }
    return render(request, 'main/new-order.html', context)


def accept(request):
    order_dict = request.session['order']

    if not settings.DEBUG:
        Order.objects.create(**order_dict)

    email = request.session['order']['email']
    context = {
        'email': email,
        'menu': menu
    }
    return render(request, 'main/accept.html', context)


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты', 'menu': menu})


def order_page(request):
    return render(request, 'main/order-page.html')


def page_not_found(request, exception):
    return render(request, 'page404.html')
