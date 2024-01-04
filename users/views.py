from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from main.models import Order


def my_orders(request):
    page = request.GET.get('page', 1)
    order_number = request.GET.get('search', False)
    query = Q(user=1)

    if order_number:
        query &= Q(order_id=order_number)

    orders = Order.objects.filter(query)
    paginator = Paginator(orders, 5)
    current_page = paginator.page(int(page))

    context = {
        'pages': current_page
    }

    return render(request, 'users/orders.html', context)
