from abc import ABC, abstractmethod


class GetCommand(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
