from abc import ABC, abstractmethod
from collections.abc import Sequence


class Registry(ABC):
    @abstractmethod
    def add(self, item) -> None:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int):
        pass

    @abstractmethod
    def get_all(self) -> Sequence:
        pass
