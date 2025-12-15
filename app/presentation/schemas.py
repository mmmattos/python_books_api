from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str | None = None

class BookOut(BaseModel):
    title: str
    author: str | None = None