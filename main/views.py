from django.shortcuts import render
from django.forms.models import model_to_dict

from main.forms import NewOrderForm
from main.utils import UtilsOrder


def index(request):
    return render(request, 'main/index.html', {'title': 'Telegram bots'})


def about(request):
    return render(request, 'main/about.html', {'title': 'О технологии'})


def prices(request):
    return render(request, 'main/prices.html', {'title': 'Цены'})


def new_order(request):
    form = NewOrderForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        order = UtilsOrder.get_order(form.cleaned_data)
        order_dict = model_to_dict(order, exclude=['date'])
        request.session.update({'order': order_dict})

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


def accept(request):
    # order_dict = request.session['order']
    # order_dict['user'] = request.user
    # if not settings.DEBUG:
    # Order.objects.create(**order_dict)

    # email = request.user.email
    # context = {
    #     'email': email,
    # }
    return render(request, 'main/accept.html')


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты'})


def order_page(request):
    return render(request, 'main/order-page.html')


def page_not_found(request, exception):
    return render(request, 'page404.html')
