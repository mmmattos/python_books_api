from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.application.books_service import BooksService
from app.presentation.dependencies import get_books_service
from app.presentation.schemas import BookCreate, BookOut

router = APIRouter()


@router.get("/books", response_model=list[BookOut])
def list_books(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: str | None = None,
    service: BooksService = Depends(get_books_service),
):
    return service.list(limit=limit, offset=offset, title=title)


@router.post("/books", response_model=BookOut, status_code=201)
def create_book(
    book: BookCreate,
    service: BooksService = Depends(get_books_service),
):
    return service.create(book.title, book.author)


@router.put("/books/{book_id}", response_model=BookOut)
def update_book(
    book_id: int,
    book: BookCreate,
    service: BooksService = Depends(get_books_service),
):
    try:
        return service.update(book_id, book.title, book.author)
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/books/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    service: BooksService = Depends(get_books_service),
):
    try:
        service.delete(book_id)
        return Response(status_code=204)
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")