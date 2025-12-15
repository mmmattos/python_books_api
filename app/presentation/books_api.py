from fastapi import APIRouter, Depends
from app.presentation.schemas import BookCreate, BookOut
from app.presentation.dependencies import get_books_service
from app.application.books_service import BooksService

router = APIRouter()

@router.get("/books", response_model=list[BookOut])
def list_books(service: BooksService = Depends(get_books_service)):
    return service.list()

@router.post("/books", status_code=201, response_model=BookOut)
def create_book(
    book: BookCreate,
    service: BooksService = Depends(get_books_service),
):
    return service.create(book.title, book.author)