from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str | None = None

class BookOut(BaseModel):
    id: int
    title: str
    author: str | None = None