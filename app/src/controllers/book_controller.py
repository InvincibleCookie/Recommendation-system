from datetime import datetime
from typing import List, Optional
from src.data_models.author import AuthorIdModel
from src.data_models.genres import GenreIdModel
from src.services.book_service import BookService
from src.data_models.book import BookFilterModel, BookModel
from fastapi import Depends, HTTPException, Query, status
from fastapi_utils.inferring_router import InferringRouter
from .common import get_array_window

book_controller_router = InferringRouter(prefix="/books", tags=["Book"])
book_service = BookService()

def get_book_service() -> BookService:
    return book_service

@book_controller_router.get("/{book_id}", response_model=BookModel)
async def get_book(book_id: int, service = Depends(get_book_service)):
    book = service.get_book(book_id)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book does't exit")

    return book

@book_controller_router.get("", response_model=list[BookModel])
async def get_books(
    titlePattern: Optional[str] = Query(None, description="Filter by book title pattern"),
    authors: Optional[List[int]] = Query(None, description="List of author IDs"),
    genres: Optional[List[int]] = Query(None, description="List of genre IDs"),
    publishDateFrom: Optional[datetime] = Query(None, description="Filter books published from this date"),
    publishDateTo: Optional[datetime] = Query(None, description="Filter books published to this date"),
    raitingFrom: Optional[float] = Query(None, description="Minimum rating"),
    raitingTo: Optional[float] = Query(None, description="Maximum rating"),
    ascendingSort: Optional[bool] = Query(None, description="Sort in ascending order"),
    sortBy: Optional[str] = Query(None, description="Sort by parameter"),
    offset: Optional[int] = Query(None, description="Number of items that will be skipped in the returned array"),
    itemCount: Optional[int] = Query(None, description="Max number of items to be returned"),
    service: BookService = Depends(get_book_service),
):
    filt = BookFilterModel(
        titlePattern=titlePattern,
        authors=[AuthorIdModel(id=author_id) for author_id in authors] if authors else None,
        genres=[GenreIdModel(id=genre_id) for genre_id in genres] if genres else None,
        publishDateFrom=publishDateFrom,
        publishDateTo=publishDateTo,
        raitingFrom=raitingFrom,
        raitingTo=raitingTo,
        ascendingSort=ascendingSort,
        sortBy=sortBy,
    )

    books = service.get_books_by_filter(filt)

    if offset is None:
        offset = 0

    if itemCount == None:
        itemCount = len(books)

    return get_array_window(books, offset, itemCount)

