from main.exceptions import OrderNotFoundException
from main.infrastructure.interfaces import ILogger
from shared.application.services.commands.delete_command import DeleteCommand
from shared.infrastructure.interfaces import IUnitOfWork


class DeleteOrder(DeleteCommand):

    def __init__(self, logger: ILogger):
        self.logger = logger

    def __call__(self, uow: IUnitOfWork, user_id: int, order_id: int):
        try:
            with uow:
                order = uow.order_repository.delete_by_id(user_id, order_id)
                if not order:
                    raise OrderNotFoundException

        except OrderNotFoundException as ex:
            raise ex
        except Exception:
            self.logger.error(f'Ошибка при удалении заказа №{order_id}')
