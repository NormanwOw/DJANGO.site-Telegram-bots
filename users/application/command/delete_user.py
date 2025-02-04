from main.infrastructure.interfaces import ILogger
from shared.application.services.commands.delete_command import DeleteCommand
from shared.infrastructure.interfaces import IUnitOfWork
from users.models import UserModel


class DeleteUser(DeleteCommand):

    def __init__(self, logger: ILogger):
        self.logger = logger

    def __call__(self, uow: IUnitOfWork, user_model: UserModel):
        try:
            with uow:
                uow.user_repository.delete(user_model)
        except Exception:
            self.logger.error(f'Ошибка при удалении пользователя {user_model.username}')
