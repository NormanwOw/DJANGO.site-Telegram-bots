from django.core.exceptions import ObjectDoesNotExist

from main.infrastructure.interfaces import IUserRepository, AbstractRepository, IOrderRepository, \
    IProductRepository
from main.models import OrderModel, ProductModel
from users.models import User


class DjangoRepository(AbstractRepository):
    model = None

    @classmethod
    def get(cls, pk):
        try:
            return cls.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create(**kwargs)

    @classmethod
    def update(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()

    @classmethod
    def all(cls):
        return cls.model.objects.all()


class UserRepository(DjangoRepository, IUserRepository):
    model = User


class OrderRepository(DjangoRepository, IOrderRepository):
    model = OrderModel


class ProductRepository(DjangoRepository, IProductRepository):
    model = ProductModel
