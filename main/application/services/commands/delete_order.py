from main.infrastructure.interfaces import ILogger
from shared.application.services.commands.delete_command import DeleteCommand
from shared.infrastructure.interfaces import IUnitOfWork


class DeleteOrder(DeleteCommand):

    def __init__(self, logger: ILogger):
        self.logger = logger

    def __call__(self, uow: IUnitOfWork, order_id: int):
        try:
            with uow:
                uow.order_repository.delete_by_id(order_id)
        except Exception:
            self.logger.error(f'Ошибка при удалении заказа №{order_id}')
