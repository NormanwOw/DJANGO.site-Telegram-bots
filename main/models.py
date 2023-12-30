from django.db import models


class Order(models.Model):
    order_id = models.IntegerField(verbose_name='Номер заказа')
    email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(verbose_name='Телефон')
    bot_shop = models.BooleanField(verbose_name='Бот-магазин', default=True)
    admin_panel = models.BooleanField(verbose_name='Админ-панель')
    database = models.BooleanField(verbose_name='База данных')
    total_price = models.IntegerField('Общая цена')
    date = models.DateTimeField(verbose_name='Дата')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.order_id)


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
