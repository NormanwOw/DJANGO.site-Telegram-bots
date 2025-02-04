from typing import List

from main.infrastructure.interfaces import ILogger
from shared.application.services.commands.get_command import GetCommand
from shared.infrastructure.interfaces import IUnitOfWork


class GetOrderNumbers(GetCommand):

    def __init__(self, logger: ILogger):
        self.logger = logger

    def __call__(self, uow: IUnitOfWork) -> List[int]:
        try:
            with uow:
                return [order.order_id for order in uow.order_repository.all()]
        except Exception:
            self.logger.error('Ошибка при получении номеров заказов')
