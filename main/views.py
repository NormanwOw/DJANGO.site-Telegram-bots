from django.shortcuts import render
from main.models import Product


menu = [{'name': 'О технологии', 'url': 'main:about'},
        {'name': 'Цены', 'url': 'main:prices'},
        {'name': 'Сделать заказ', 'url': 'main:new-order'},
        {'name': 'Контакты', 'url': 'main:contacts'}]


def index(request):
    return render(request, 'main/index.html', {'title': 'Telegram bots', 'menu': menu})


def about(request):
    return render(request, 'main/about.html', {'title': 'О технологии', 'menu': menu})


def prices(request):
    price_list = Product.objects.all()
    context = {
        'title': 'Цены',
        'menu': menu,
        'price_list': price_list
    }
    return render(request, 'main/prices.html', context)


def new_order(request):
    return render(request, 'main/new-order.html')


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты', 'menu': menu})


def order_page(request):
    return render(request, 'main/order-page.html')


def page_not_found(request, exception):
    return render(request, 'main/page404.html')
