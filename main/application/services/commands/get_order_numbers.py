from typing import List

from shared.application.services.commands.get_command import GetCommand
from shared.infrastructure.interfaces import IUnitOfWork


class GetOrderNumbers(GetCommand):

    def __call__(self, uow: IUnitOfWork) -> List[int]:
        with uow:
            return [order.order_id for order in uow.order_repository.all()]
