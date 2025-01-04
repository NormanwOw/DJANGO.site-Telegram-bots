from abc import ABC, abstractmethod

from main.infrastructure.interfaces import IUserRepository, IOrderRepository, IProductRepository


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
