from django.db import models
from datetime import datetime

from phonenumber_field.modelfields import PhoneNumberField

from users.models import User


class Product(models.Model):
    name = models.CharField(verbose_name='Товар')
    price = models.IntegerField(verbose_name='Цена')
    title = models.CharField(verbose_name='Название')
    description = models.CharField(verbose_name='Описание', default='...')

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS = {
        ('ordered', 'Оформлен'),
        ('in_progress', 'В работе'),
        ('completed', 'Исполнен')
    }

    order_id = models.IntegerField(verbose_name='Номер заказа')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone_number = PhoneNumberField(region='RU', verbose_name='Телефон')
    bot_shop = models.IntegerField(verbose_name='Бот-магазин')
    admin_panel = models.IntegerField(verbose_name='Админ-панель')
    database = models.IntegerField(verbose_name='База данных')
    total_price = models.IntegerField('Общая цена')
    date = models.DateTimeField(verbose_name='Дата', default=datetime.utcnow)
    status = models.CharField(verbose_name='Статус', choices=STATUS, default='ordered')

    product_list = Product.objects.all()

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-date']

    def __str__(self):
        return str(self.order_id)

    def __iter__(self):
        for field in self._meta.fields:
            title = field.verbose_name
            if title not in ['ID', 'Дата', 'Номер заказа']:
                yield title, field.value_to_string(self)

    def get_products(self) -> list:
        return [(product.title, getattr(self, product.name)) for product in self.product_list]


class Menu(models.Model):
    name = models.CharField(verbose_name='Название')
    url = models.CharField(verbose_name='Ссылка')

    class Meta:
        db_table = 'menu'
        verbose_name = 'Меню'


class Contact(models.Model):
    title = models.CharField()
    str_image = models.CharField()
    value = models.CharField()

    class Meta:
        db_table = 'contact'
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
