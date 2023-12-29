from django.db import models


class Order(models.Model):
    order_id = models.IntegerField(verbose_name='Номер заказа')
    email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(verbose_name='Телефон')
    bot_shop = models.IntegerField(verbose_name='Бот магазин')
    admin_panel = models.IntegerField(verbose_name='Админ панель')
    database = models.IntegerField(verbose_name='База данных')
    total_price = models.IntegerField('Общая цена')
    date = models.DateTimeField(verbose_name='Дата')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Product(models.Model):
    product = models.CharField(verbose_name='Товар')
    price = models.IntegerField(verbose_name='Цена')
    title = models.CharField(verbose_name='Название')
    description = models.CharField(verbose_name='Описание', default='...')

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
