from fastapi import HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.data_models.author import AuthorFilterModel, AuthorIdModel, AuthorModel
from src.services.author_service import AuthorService


author_controller_router = InferringRouter()

@cbv(author_controller_router)
class AurhorController:
    def __init__(self):
        self.author_service = AuthorService()

    @author_controller_router.post("/get/one", response_model=AuthorModel)
    async def get_author(self, author_id: AuthorIdModel):
        author = self.author_service.get_author(author_id.id)

        if author is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author does't exits")

        return author

    @author_controller_router.post("/get/filt", response_model=list[AuthorModel])
    async def get_authors(self, filt: AuthorFilterModel):
        return self.author_service.get_authors_by_filter(filt)
