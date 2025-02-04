from main.domain.aggregates import Order
from shared.application.services.commands.command import Command
from shared.application.services.commands.create_command import CreateCommand
from shared.infrastructure.interfaces import IUnitOfWork
from main.infrastructure.interfaces import ILogger


class CreateOrderService:

    def __init__(
            self,
            create_order: CreateCommand,
            send_email: Command,
            uow: IUnitOfWork,
            logger: ILogger
    ):
        self.create_order = create_order
        self.send_email = send_email
        self.uow = uow
        self.logger = logger

    def execute(self, order: Order):
        self.logger.info(f'Получен заказ №{order.number}')
        updated_order = self.create_order(self.uow, order)
        self.logger.info(f'Заказ №{order.number} создан')
        self.send_email(updated_order)
        self.logger.info(f'Информация с заказом №{order.number} отправлена на почту {order.email}')
