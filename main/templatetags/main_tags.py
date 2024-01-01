from django import template
from main.models import Menu, Product, Contact


register = template.Library()


@register.simple_tag()
def menu():
    return Menu.objects.all()


@register.simple_tag()
def price_list():
    return Product.objects.all()


@register.simple_tag()
def contact_list():
    return Contact.objects.all()
