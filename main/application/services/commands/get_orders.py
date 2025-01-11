from typing import List

from main.domain.aggregates import Order
from shared.application.services.commands.get_command import GetCommand
from shared.infrastructure.interfaces import IUnitOfWork


class GetOrders(GetCommand):

    def __call__(self, uow: IUnitOfWork, user_id: int) -> List[Order]:
        with uow:
            orders = uow.order_repository.get_by_user_id(user_id)
            return [order.to_domain() for order in orders]
