from shared.application.services.commands.delete_command import DeleteCommand
from shared.infrastructure.interfaces import IUnitOfWork
from users.models import UserModel


class DeleteUser(DeleteCommand):

    def __call__(self, uow: IUnitOfWork, user_model: UserModel):
        with uow:
            uow.user_repository.delete(user_model)
