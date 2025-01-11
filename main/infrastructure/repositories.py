from typing import List

from main.domain.aggregates import Order
from main.domain.entities import Product
from main.infrastructure.interfaces import IUserRepository, IOrderRepository, IProductRepository
from main.infrastructure.models import OrderModel, ProductModel
from users.domain.entities import User
from users.models import UserModel


class UserRepository(IUserRepository):
    model = UserModel

    @classmethod
    def get(cls, user: User) -> UserModel:
        return cls.model.objects.get(pk=user.id)

    @classmethod
    def create(cls, user: User) -> UserModel:
        raise NotImplementedError

    @classmethod
    def update(cls, user: User, user_model: UserModel) -> UserModel:
        user_model.username = user.username
        user_model.email = user.email
        user_model.first_name = user.first_name
        user_model.last_name = user.last_name
        user_model.is_active = user.is_active
        user_model.is_staff = user.is_staff
        user_model.is_superuser = user.is_superuser
        user_model.save()
        return user_model

    @classmethod
    def delete(cls, user_model: UserModel):
        cls.model.delete(user_model)

    @classmethod
    def all(cls) -> List[UserModel]:
        return cls.model.objects.all()


class OrderRepository(IOrderRepository):
    model = OrderModel

    @classmethod
    def get(cls, order: Order) -> OrderModel:
        return cls.model.objects.get(order_id=order.number)

    @classmethod
    def get_by_user_id(cls, user_id: int) -> List[OrderModel]:
        return cls.model.objects.filter(user_id=user_id)

    @classmethod
    def create(cls, order: Order) -> OrderModel:
        order_model = cls.model.from_domain(order)
        order_model.save()
        return order_model

    @classmethod
    def update(cls, order: Order, order_model: OrderModel) -> OrderModel:
        order_model.order_id = order.number
        order_model.phone_number = order.phone_number
        order_model.total_price = order.total_price
        order_model.save()
        return order_model

    @classmethod
    def delete(cls, order_model: OrderModel):
        cls.model.delete(order_model)

    @classmethod
    def delete_by_id(cls, order_id: int):
        cls.model.objects.filter(order_id=order_id).delete()

    @classmethod
    def all(cls) -> List[OrderModel]:
        return cls.model.objects.all()


class ProductRepository(IProductRepository):
    model = ProductModel

    @classmethod
    def get(cls, product: Product) -> ProductModel:
        return cls.model.objects.get(code=product.code)

    @classmethod
    def get_by_code(cls, code_list: list[str]) -> List[ProductModel]:
        return cls.model.objects.filter(code__in=code_list)

    @classmethod
    def get_by_name(cls, product_name: str) -> ProductModel:
        return cls.model.objects.filter(name=product_name).first()

    @classmethod
    def create(cls, product: Product) -> ProductModel:
        product_model = cls.model.from_domain(product)
        product_model.save()
        return product_model

    @classmethod
    def update(cls, product: Product, product_model: ProductModel) -> ProductModel:
        product_model.code = product.code
        product_model.name = product.name
        product_model.price = product.price
        product_model.title = product.title
        product_model.description = product.description
        product_model.save()
        return product_model

    @classmethod
    def delete(cls, product_model: ProductModel):
        cls.model.delete(product_model)

    @classmethod
    def all(cls) -> List[ProductModel]:
        return cls.model.objects.all()
