from django.core.paginator import Paginator
from django.shortcuts import render
from main.models import Order


def my_orders(request):

    page = request.GET.get('page', 1)
    orders = Order.objects.filter(user=1)
    paginator = Paginator(orders, 5)
    current_page = paginator.page(int(page))
    context = {
        'pages': current_page,
    }
    return render(request, 'users/my-orders.html', context)
