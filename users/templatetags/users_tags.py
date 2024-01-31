from django import template
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.http import urlencode
from django.shortcuts import Http404

from main.models import Order

register = template.Library()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)

    return '?' + urlencode(query)


@register.simple_tag(takes_context=True)
def get_order_page(context):
    request = context['request']
    order_id = request.GET.get('remove-order', False)

    if order_id:
        result = Order.objects.filter(order_id=order_id, user=request.user).delete()

        if not result[0]:
            raise Http404()

    page = request.GET.get('page', 1)
    order_number = request.GET.get('search', False)
    query = Q(user=request.user.id)

    if order_number:
        query &= Q(order_id__contains=order_number)

    orders = Order.objects.filter(query)
    paginator = Paginator(orders, 3)
    current_page = paginator.page(int(page))

    return current_page
