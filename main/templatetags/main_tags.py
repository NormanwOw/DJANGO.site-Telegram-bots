from django import template
from main.infrastructure.models import MenuModel, ProductModel, ContactModel


register = template.Library()


@register.simple_tag()
def menu():
    return MenuModel.objects.all()


@register.simple_tag()
def product_list():
    return ProductModel.objects.all()


@register.simple_tag()
def contact_list():
    return ContactModel.objects.all()
