from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.forms import NewOrderForm
from main.utils import UtilsOrder
from main.models import Order


def index(request):
    return render(request, 'main/index.html', {'title': 'Telegram bots'})


def about(request):
    return render(request, 'main/about.html', {'title': 'О технологии'})


def prices(request):
    return render(request, 'main/prices.html', {'title': 'Цены'})


@login_required
def new_order(request):
    form = NewOrderForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        order_dict = UtilsOrder.get_order(form.cleaned_data)
        request.session.update({'order': order_dict})
        order = Order(**order_dict)

        context = {
            'new_order': order,
        }

        return render(request, 'main/accept.html', context)
    else:
        form = NewOrderForm()

    context = {
        'title': 'Новый заказ',
        'form': form
    }
    return render(request, 'main/new-order.html', context)


@login_required
def accept(request):
    order_dict = request.session['order']
    order_dict['user'] = request.user
    Order.objects.create(**order_dict)

    order_number = order_dict['order_id']
    email = request.user.email
    context = {
        'email': email,
        'order_number': order_number
    }
    return render(request, 'main/accept.html', context)


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты'})


def page_not_found(request, exception):
    return render(request, 'page404.html')
