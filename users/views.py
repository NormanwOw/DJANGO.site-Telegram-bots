from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from main.models import Order
from users.forms import LoginForm


@login_required
def my_orders(request):
    page = request.GET.get('page', 1)
    order_number = request.GET.get('search', False)
    query = Q(user=request.user.id)

    if order_number:
        query &= Q(order_id=order_number)

    orders = Order.objects.filter(query)
    paginator = Paginator(orders, 5)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Мои заказы',
        'pages': current_page
    }

    return render(request, 'users/orders.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse('main:home'))
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    context = {
        'title': 'Регистрация',
    }
    return render(request, 'users/registration.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:home'))
