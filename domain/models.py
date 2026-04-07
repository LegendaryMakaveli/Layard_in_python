from dataclasses import dataclass
from typing import Optional

@dataclass
class Todo:
    title: str
    description: str
    completed: bool = False
    id: Optional[int] = None
