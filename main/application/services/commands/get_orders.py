from typing import List

from django.contrib.auth.models import User

from main.domain.aggregates import Order
from main.infrastructure.interfaces import ILogger
from shared.application.services.commands.get_command import GetCommand
from shared.infrastructure.interfaces import IUnitOfWork


class GetOrders(GetCommand):

    def __init__(self, logger: ILogger):
        self.logger = logger

    def __call__(self, uow: IUnitOfWork, user: User) -> List[Order]:
        try:
            with uow:
                orders = uow.order_repository.get_by_user_id(user.pk)
                return [order.to_domain(user.email) for order in orders]
        except Exception:
            self.logger.error(f'Ошибка при получении заказов у пользователя {user.email}')
