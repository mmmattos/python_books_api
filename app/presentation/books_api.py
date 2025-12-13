from fastapi import APIRouter
from app.presentation.schemas import BookCreate, BookOut
from app.infrastructure.in_memory_book_repository import InMemoryBookRepository
from app.application.books_service import BooksService

router = APIRouter()

repo = InMemoryBookRepository()
service = BooksService(repo)

@router.get("/books", response_model=list[BookOut])
def list_books():
    return service.list_books()

@router.post("/books", response_model=BookOut, status_code=201)
def create_book(book: BookCreate):
    return service.create_book(book.title, book.author)