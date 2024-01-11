from django.contrib import admin
from main.models import Order, Product


class OrderTabularAdmin(admin.TabularInline):
    model = Order

    readonly_fields = ('date',)
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'order_id', 'user', 'phone_number', 'total_price', 'status', 'date'
    search_fields = ('order_id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'title', 'price', 'description'
    search_fields = ('title',)

