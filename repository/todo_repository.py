from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import Todo

class TodoRepository(ABC):
    @abstractmethod
    def add(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    def get(self, todo_id: int) -> Optional[Todo]:
        pass

    @abstractmethod
    def get_all(self) -> List[Todo]:
        pass

    @abstractmethod
    def update(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    def delete(self, todo_id: int) -> bool:
        pass
