from django.shortcuts import render

menu = [{'name': 'О технологии', 'url': 'about'},
        {'name': 'Цены', 'url': 'prices'},
        {'name': 'Сделать заказ', 'url': 'new-order'},
        {'name': 'Контакты', 'url': 'contacts'}]


def index(request):
    return render(request, 'main/index.html', {'title': 'Telegram bots', 'menu': menu})


def about(request):
    return render(request, 'main/about.html', {'title': 'О технологии', 'menu': menu})


def prices(request):
    return render(request, 'main/prices.html')


def new_order(request):
    return render(request, 'main/new-order.html')


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты', 'menu': menu})


def order_page(request):
    return render(request, 'main/order-page.html')


def page_not_found(request, exception):
    return render(request, 'main/page404.html')
