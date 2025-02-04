from abc import ABC, abstractmethod
from typing import List

from main.domain.aggregates import Order
from main.domain.entities import Product
from main.infrastructure.models import OrderModel, ProductModel
from users.domain.entities import User
from users.models import UserModel


class IUserRepository(ABC):
    model = None

    @classmethod
    @abstractmethod
    def get(cls, user: User) -> UserModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, user: User, user_model: UserModel) -> UserModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete(cls, user_model: UserModel):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def all(cls) -> List[UserModel]:
        raise NotImplementedError


class IOrderRepository(ABC):
    model = None

    @classmethod
    @abstractmethod
    def get(cls, order: Order) -> OrderModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_by_user_id(cls, user_id: int) -> List[OrderModel]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, order: Order) -> OrderModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, order: Order, order_model: OrderModel) -> OrderModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete(cls, order_model: OrderModel):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete_by_id(cls, order_id: int):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def all(cls) -> List[OrderModel]:
        raise NotImplementedError


class IProductRepository(ABC):
    model = None

    @classmethod
    @abstractmethod
    def get(cls, product: Product) -> ProductModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_by_code(cls, code_list: list[str]) -> List[ProductModel]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_by_name(cls, product_name: str) -> ProductModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, product: Product) -> ProductModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, product: Product, product_model: ProductModel) -> ProductModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete(cls, product_model: ProductModel):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def all(cls) -> List[ProductModel]:
        raise NotImplementedError


class ILogger(ABC):

    @abstractmethod
    def info(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def warning(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def debug(self, message: str):
        raise NotImplementedError
