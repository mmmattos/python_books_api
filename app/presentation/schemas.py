from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None


class BookUpdate(BaseModel):
    title: str
    author: Optional[str] = None


class BookOut(BaseModel):
    id: int
    title: str
    author: Optional[str] = None