from fastapi import APIRouter, Depends
from app.presentation.dependencies import get_books_service
from app.application.books_service import BooksService

router = APIRouter()


@router.get("/books")
def list_books(service: BooksService = Depends(get_books_service)):
    return service.list()


@router.post("/books", status_code=201)
def create_book(
    book: dict,
    service: BooksService = Depends(get_books_service),
):
    # DO NOT add here
    return service.create(book["title"], book["author"])