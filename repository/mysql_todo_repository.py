import mysql.connector
from typing import List, Optional
from data.models import Todo
from repository.todo_repository import TodoRepository
import os

class MySQLTodoRepository(TodoRepository):
    def __init__(self, **db_config):
        self.db_config = db_config
        self._init_db()

    def _get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def _init_db(self):
        config_no_db = self.db_config.copy()
        db_name = config_no_db.pop('database', 'todos')

        with mysql.connector.connect(**config_no_db) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS todos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        completed BOOLEAN NOT NULL DEFAULT 0
                    )
                ''')
            conn.commit()

    def add(self, todo: Todo) -> Todo:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO todos (title, description, completed) VALUES (%s, %s, %s)',
                    (todo.title, todo.description, todo.completed)
                )
                todo.id = cursor.lastrowid
            conn.commit()
            return todo

    def get(self, todo_id: int) -> Optional[Todo]:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, title, description, completed FROM todos WHERE id = %s', (todo_id,))
                row = cursor.fetchone()
                if row:
                    return Todo(id=row[0], title=row[1], description=row[2], completed=bool(row[3]))
                return None

    def get_all(self) -> List[Todo]:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, title, description, completed FROM todos ORDER BY id ASC')
                rows = cursor.fetchall()
                return [Todo(id=row[0], title=row[1], description=row[2], completed=bool(row[3])) for row in rows]

    def update(self, todo: Todo) -> Todo:
        if todo.id is None:
            raise ValueError("Todo ID cannot be None for update")
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE todos SET title = %s, description = %s, completed = %s WHERE id = %s',
                    (todo.title, todo.description, todo.completed, todo.id)
                )
            conn.commit()
            return todo

    def delete(self, todo_id: int) -> bool:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
                deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
