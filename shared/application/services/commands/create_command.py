from abc import ABC, abstractmethod


class CreateCommand(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
