from typing import Optional
from fastapi import Depends, HTTPException, Query, status
from fastapi_utils.inferring_router import InferringRouter

from src.data_models.author import AuthorFilterModel, AuthorModel
from src.services.author_service import AuthorService
from .common import get_array_window


author_controller_router = InferringRouter(prefix="/authors", tags=["Author"])
author_service = AuthorService()

def get_author_service() -> AuthorService:
    return author_service

@author_controller_router.get("/{author_id}", response_model=AuthorModel)
async def get_author(author_id: int, service = Depends(get_author_service)):
    author = service.get_author(author_id)

    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author does't exits")

    return author

@author_controller_router.get("", response_model=list[AuthorModel])
async def get_authors(
    namePattern: Optional[str] = Query(None, description="Filter by author name"),
    ascendingSort: Optional[bool] = Query(None, description="Sort in ascending order"),
    sortBy: Optional[str] = Query(None, description="Sort by parameter"),
    offset: Optional[int] = Query(None, description="Number of items that will be skipped in the returned array"),
    itemCount: Optional[int] = Query(None, description="Max number of items to be returned"),
    service: AuthorService = Depends(get_author_service)
):
    filt = AuthorFilterModel(
        namePattern=namePattern if namePattern is not None else "%",
        sortBy=sortBy,
        ascendingSort=ascendingSort,
    )

    authors = service.get_authors_by_filter(filt)
    if offset is None:
        offset = 0

    if itemCount == None:
        itemCount = len(authors)

    return get_array_window(authors, offset, itemCount)
