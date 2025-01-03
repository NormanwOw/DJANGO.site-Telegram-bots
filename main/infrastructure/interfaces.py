from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @classmethod
    def get(cls, pk):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def update(cls, instance, **kwargs):
        raise NotImplementedError

    @classmethod
    def delete(cls, instance):
        raise NotImplementedError

    @classmethod
    def all(cls):
        raise NotImplementedError


class IUserRepository(AbstractRepository, ABC):
    pass


class IOrderRepository(AbstractRepository, ABC):
    pass


class IProductRepository(AbstractRepository, ABC):
    pass


class IUnitOfWork(ABC):
    user_repository: IUserRepository
    order_repository: IOrderRepository
    product_repository: IProductRepository

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, traceback) -> bool:
        raise NotImplementedError
