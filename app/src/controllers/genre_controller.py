from fastapi import HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.data_models.genres import GenreFilterModel, GenreModel, GenreIdModel
from src.services.genre_service import GenreService


genre_controller_router = InferringRouter()

@cbv(genre_controller_router)
class GenreController:
    def __init__(self):
        self.genre_service = GenreService()

    @genre_controller_router.post("/get/one", response_model=GenreModel)
    async def get_genre(self, genre_id: GenreIdModel):
        genre = self.genre_service.get_genre(genre_id.id)

        if genre is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre does't exits")

        return genre

    @genre_controller_router.post("/get/filt", response_model=list[GenreModel])
    async def get_authors(self, filt: GenreFilterModel):
        return self.genre_service.get_genres_by_filt(filt)
