from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Order(models.Model):
    order_id = models.IntegerField(verbose_name='Номер заказа')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
