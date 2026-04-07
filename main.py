import os
from dotenv import load_dotenv
from repository.mysql_todo_repository import MySQLTodoRepository
from service.todo_service import TodoService
from presentation.console_interface import ConsoleInterface

def main():
    load_dotenv()
    
    db_config = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "database": os.environ.get("DB_NAME", "todos")
    }
    
    try:
        repository = MySQLTodoRepository(**db_config)
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        print("Please ensure your SQL server is running and credentials are valid.")
        return

    service = TodoService(repository)
    
    app_interface = ConsoleInterface(service)
    
    app_interface.run()

if __name__ == "__main__":
    main()
