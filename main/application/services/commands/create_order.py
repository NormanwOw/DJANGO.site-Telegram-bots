from main.domain.aggregates import Order
from shared.infrastructure.interfaces import IUnitOfWork
from shared.application.services.commands.create_command import CreateCommand


class CreateOrder(CreateCommand):

    def __call__(self, uow: IUnitOfWork, order: Order):
        with uow:
            bot_shop = uow.product_repository.get_by_name('bot_shop')
            order.total_price += bot_shop.price
            order_model = uow.order_repository.create(order)
            code_list = [product.code for product in order.products]
            products = list(uow.product_repository.get_by_code(code_list))
            products.append(bot_shop)
            order_model.products.add(*products)
