from django.contrib import admin
from main.infrastructure.models import OrderModel, ProductModel


class OrderTabularAdmin(admin.TabularInline):
    model = OrderModel

    readonly_fields = ('date',)
    extra = 1


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'order_id', 'user', 'phone_number', 'total_price', 'status', 'date'
    search_fields = ('order_id',)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'title', 'price', 'description'
    search_fields = ('title',)
