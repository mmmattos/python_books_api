from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    id: Optional[int] = None
    title: str = ""
    author: Optional[str] = None