from src.services.book_service import BookService
from src.data_models.book import BookFilterModel, BookIdModel, FullBookModel
from fastapi import HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

book_controller_router = InferringRouter()

@cbv(book_controller_router)
class BookController:
    def __init__(self):
        self.book_service = BookService()

    @book_controller_router.post("/get", response_model=FullBookModel)
    async def get_book(self, book_id: BookIdModel):
        book = self.book_service.get_book(book_id.id)

        if book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book does't exit")

        return book

    @book_controller_router.post("/filter", response_model=list[FullBookModel])
    async def filter_books(self, filt: BookFilterModel):
        return self.book_service.get_books_by_filter(filt)

