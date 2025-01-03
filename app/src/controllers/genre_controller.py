from typing import Optional
from fastapi import Depends, HTTPException, Query, status
from fastapi_utils.inferring_router import InferringRouter

from src.data_models.genres import GenreFilterModel, GenreModel
from src.services.genre_service import GenreService
from .common import get_array_window


genre_controller_router = InferringRouter(prefix="/genres", tags=["Genre"])
genre_service = GenreService()

def get_genre_service() -> GenreService:
    return genre_service

@genre_controller_router.get("/{genre_id}", response_model=GenreModel)
async def get_genre(genre_id: int, service = Depends(get_genre_service)):
    genre = service.get_genre(genre_id)

    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre does't exits")

    return genre

@genre_controller_router.get("", response_model=list[GenreModel])
async def get_genres(
    namePattern: Optional[str] = Query(None, description="Filter by author name"),
    ascendingSort: Optional[bool] = Query(None, description="Sort in ascending order"),
    sortBy: Optional[str] = Query(None, description="Sort by parameter"),
    offset: Optional[int] = Query(None, description="Number of items that will be skipped in the returned array"),
    itemCount: Optional[int] = Query(None, description="Max number of items to be returned"),
    service = Depends(get_genre_service)
):
    filt = GenreFilterModel(
        namePattern=namePattern if namePattern is not None else "%",
        ascendingSort=ascendingSort,
        sortBy=sortBy,
    )

    genres = service.get_genres_by_filt(filt)
    if offset is None:
        offset = 0

    if itemCount == None:
        itemCount = len(genres)

    return get_array_window(genres, offset, itemCount)
