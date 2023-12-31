from django.db import models
from datetime import datetime


class Order(models.Model):
    order_id = models.IntegerField(verbose_name='Номер заказа')
    email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(verbose_name='Телефон')
    bot_shop = models.BooleanField(verbose_name='Бот-магазин', default=True)
    admin_panel = models.BooleanField(verbose_name='Админ-панель')
    database = models.BooleanField(verbose_name='База данных')
    total_price = models.IntegerField('Общая цена')
    date = models.DateTimeField(verbose_name='Дата', default=datetime.utcnow)

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.order_id)

    def __iter__(self):
        for field in self._meta.fields:
            title = field.verbose_name
            if title not in ['ID', 'Дата', 'Номер заказа']:
                yield title, field.value_to_string(self)


class Product(models.Model):
    product = models.CharField(verbose_name='Товар')
    price = models.IntegerField(verbose_name='Цена')
    title = models.CharField(verbose_name='Название')
    description = models.CharField(verbose_name='Описание', default='...')

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title
