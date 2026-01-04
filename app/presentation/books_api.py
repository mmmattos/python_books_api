from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.books_service import BooksService
from app.presentation.schemas import BookCreate, BookOut, BookUpdate
from app.presentation.dependencies import get_books_service

router = APIRouter()


@router.get(
    "/books",
    response_model=List[BookOut],
)
def list_books(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: Optional[str] = None,
    sort: Optional[str] = None,
    service: BooksService = Depends(get_books_service),
):
    return service.list(limit, offset, title, sort)


@router.post(
    "/books",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    book: BookCreate,
    service: BooksService = Depends(get_books_service),
):
    return service.create(book.title, book.author)


@router.put(
    "/books/{book_id}",
    response_model=BookOut,
)
def update_book(
    book_id: int,
    book: BookUpdate,
    service: BooksService = Depends(get_books_service),
):
    updated = service.update(book_id, book.title, book.author)
    if updated is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    book_id: int,
    service: BooksService = Depends(get_books_service),
):
    if not service.delete(book_id):
        raise HTTPException(status_code=404, detail="Book not found")