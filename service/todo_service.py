from typing import List, Optional
from domain.models import Todo
from repository.todo_repository import TodoRepository

class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def create_todo(self, title: str, description: str = "") -> Todo:
        todo = Todo(title=title, description=description)
        return self.repository.add(todo)

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        return self.repository.get(todo_id)

    def list_todos(self) -> List[Todo]:
        return self.repository.get_all()

    def mark_completed(self, todo_id: int) -> Optional[Todo]:
        todo = self.repository.get(todo_id)
        if todo:
            todo.completed = True
            return self.repository.update(todo)
        return None

    def delete_todo(self, todo_id: int) -> bool:
        return self.repository.delete(todo_id)
