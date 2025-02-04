from django.db import models
from datetime import datetime

from phonenumber_field.modelfields import PhoneNumberField

from main.domain.aggregates import Order
from main.domain.entities import Product
from users.models import UserModel


class ProductModel(models.Model):
    code = models.CharField(verbose_name='Код')
    name = models.CharField(verbose_name='Товар')
    price = models.IntegerField(verbose_name='Цена')
    title = models.CharField(verbose_name='Название')
    description = models.CharField(verbose_name='Описание', default='...')

    class Meta:
        db_table = 'product'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = 'pk',

    def __str__(self):
        return self.title

    def to_domain(self) -> Product:
        return Product(
            id=self.pk,
            code=self.code,
            name=self.name,
            price=self.price,
            title=self.title,
            description=self.description
        )

    @staticmethod
    def from_domain(product: Product) -> 'ProductModel':
        return ProductModel(
            id=product.id,
            code=product.code,
            name=product.name,
            price=product.price,
            title=product.title,
            description=product.description
        )


class OrderModel(models.Model):
    STATUS = {
        ('Оформлен', 'Оформлен'),
        ('В работе', 'В работе'),
        ('Исполнен', 'Исполнен')
    }

    order_id = models.IntegerField(verbose_name='Номер заказа')
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='orders'
    )
    phone_number = PhoneNumberField(region='RU', verbose_name='Телефон')
    total_price = models.IntegerField('Общая цена')
    date = models.DateTimeField(verbose_name='Дата', default=datetime.utcnow)
    status = models.CharField(verbose_name='Статус', choices=STATUS, default='Оформлен')
    products = models.ManyToManyField(ProductModel)

    class Meta:
        db_table = 'order'
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['-date']

    def __str__(self):
        return str(self.order_id)

    def __iter__(self):
        for field in self._meta.fields:
            title = field.verbose_name
            if title not in ['ID', 'Дата', 'Номер заказа']:
                yield title, field.value_to_string(self)

    def to_domain(self, email: str) -> Order:
        return Order(
            number=self.order_id,
            phone_number=str(self.phone_number),
            user_id=self.user.pk,
            email=email,
            total_price=self.total_price,
            status=self.status,
            products=[product.to_domain() for product in self.products.all()],
            date=self.date
        )

    @staticmethod
    def from_domain(order: Order) -> 'OrderModel':
        order_model = OrderModel(
            order_id=order.number,
            phone_number=order.phone_number,
            user=UserModel.objects.get(pk=order.user_id),
            status=order.status,
            total_price=order.total_price,
            date=order.date
        )
        return order_model


class MenuModel(models.Model):
    name = models.CharField(verbose_name='Название')
    url = models.CharField(verbose_name='Ссылка')

    class Meta:
        db_table = 'menu'
        verbose_name = 'меню'


class ContactModel(models.Model):
    title = models.CharField()
    str_image = models.CharField()
    value = models.CharField()

    class Meta:
        db_table = 'contact'
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        ordering = ('pk',)
