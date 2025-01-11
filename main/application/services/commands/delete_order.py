from shared.application.services.commands.delete_command import DeleteCommand
from shared.infrastructure.interfaces import IUnitOfWork


class DeleteOrder(DeleteCommand):

    def __call__(self, uow: IUnitOfWork, order_id: int):
        with uow:
            uow.order_repository.delete_by_id(order_id)
