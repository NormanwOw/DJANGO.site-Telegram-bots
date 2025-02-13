from django.db import transaction

from main.infrastructure.repositories import UserRepository, OrderRepository, ProductRepository
from shared.infrastructure.interfaces import IUnitOfWork


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.user_repository = UserRepository()
        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()

    def __enter__(self):
        transaction.set_autocommit(False)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type:
            transaction.rollback()
            return
        transaction.commit()
        transaction.set_autocommit(True)


class TestUnitOfWork(IUnitOfWork):

    def __init__(self):
        self.user_repository = UserRepository()
        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass
