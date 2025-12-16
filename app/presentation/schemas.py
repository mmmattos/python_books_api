from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None

class BookOut(BookCreate):
    id: int