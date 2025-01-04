from abc import ABC

from shared.application.services.commands.command import Command


class DeleteCommand(Command, ABC):
    pass
