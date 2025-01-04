from main.domain.aggregates import Order
from shared.infrastructure.interfaces import IUnitOfWork
from shared.application.services.commands.create_command import CreateCommand


class CreateOrder(CreateCommand):

    def __call__(self, uow: IUnitOfWork, order: Order):
        with uow:
            order_model = uow.order_repository.create(order)
            code_list = [product.code for product in order.products]
            products = uow.product_repository.get_by_code(code_list)
            order_model.products.add(*products)
