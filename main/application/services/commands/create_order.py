from main.domain.aggregates import Order
from main.infrastructure.interfaces import ILogger
from shared.infrastructure.interfaces import IUnitOfWork
from shared.application.services.commands.create_command import CreateCommand


class CreateOrder(CreateCommand):

    def __init__(self, logger: ILogger):
        self.logger = logger

    def __call__(self, uow: IUnitOfWork, order: Order) -> Order:
        try:
            with uow:
                bot_shop = uow.product_repository.get_by_name('bot_shop')
                if bot_shop:
                    order.total_price += bot_shop.price
                order_model = uow.order_repository.create(order)
                code_list = [product.code for product in order.products]
                products = list(uow.product_repository.get_by_code(code_list))
                if bot_shop:
                    products.append(bot_shop)
                order_model.products.add(*products)
                return order_model.to_domain(order.email)
        except Exception:
            self.logger.error(f'Ошибка при создании заказа №{order.number} у пользователя {order.email}')
