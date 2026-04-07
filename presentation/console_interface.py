from service.todo_service import TodoService

class ConsoleInterface:
    def __init__(self, service: TodoService):
        self.service = service

    def run(self):
        while True:
            print("\n--- Todo App ---")
            print("1. List Todos")
            print("2. Add Todo")
            print("3. Mark Completed")
            print("4. Delete Todo")
            print("5. Exit")
            
            choice = input("Select an option: ")
            
            if choice == '1':
                self._list_todos()
            elif choice == '2':
                self._add_todo()
            elif choice == '3':
                self._mark_completed()
            elif choice == '4':
                self._delete_todo()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

    def _list_todos(self):
        todos = self.service.list_todos()
        if not todos:
            print("No todos found.")
            return
        
        for t in todos:
            status = "[x]" if t.completed else "[ ]"
            print(f"{t.id}. {status} {t.title} - {t.description}")

    def _add_todo(self):
        title = input("Enter title: ")
        if not title:
            print("Title cannot be empty.")
            return
        description = input("Enter description: ")
        todo = self.service.create_todo(title, description)
        print(f"Todo '{todo.title}' created with ID {todo.id}.")

    def _mark_completed(self):
        todo_id = input("Enter Todo ID to complete: ")
        try:
            todo_id_int = int(todo_id)
            updated_todo = self.service.mark_completed(todo_id_int)
            if updated_todo:
                print(f"Todo {todo_id_int} marked as completed.")
            else:
                print(f"Todo {todo_id_int} not found.")
        except ValueError:
            print("Invalid ID.")

    def _delete_todo(self):
        todo_id = input("Enter Todo ID to delete: ")
        try:
            todo_id_int = int(todo_id)
            success = self.service.delete_todo(todo_id_int)
            if success:
                print(f"Todo {todo_id_int} deleted.")
            else:
                print(f"Todo {todo_id_int} not found.")
        except ValueError:
            print("Invalid ID.")
