from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.books_service import BooksService
from app.presentation.dependencies import get_books_service
from app.presentation.schemas import BookCreate, BookOut

router = APIRouter(tags=["books"])


@router.get("/books", response_model=List[BookOut])
def list_books(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: Optional[str] = Query(None),
    sort: Optional[str] = Query(
        None,
        description="Sort by field: id, title, author. Prefix with '-' for DESC.",
    ),
    service: BooksService = Depends(get_books_service),
):
    return service.list(
        limit=limit,
        offset=offset,
        title=title,
        sort=sort,
    )


@router.post(
    "/books",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    book: BookCreate,
    service: BooksService = Depends(get_books_service),
):
    return service.create(
        title=book.title,
        author=book.author,
    )


@router.get("/books/{book_id}", response_model=BookOut)
def get_book(
    book_id: int,
    service: BooksService = Depends(get_books_service),
):
    book = service.get(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.put("/books/{book_id}", response_model=BookOut)
def update_book(
    book_id: int,
    book: BookCreate,
    service: BooksService = Depends(get_books_service),
):
    updated = service.update(
        book_id=book_id,
        title=book.title,
        author=book.author,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return updated


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    service: BooksService = Depends(get_books_service),
):
    deleted = service.delete(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )