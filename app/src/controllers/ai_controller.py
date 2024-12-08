from fastapi import Depends, HTTPException, Query, status
from fastapi_utils.inferring_router import InferringRouter

from src.ai.book import BookAI
from src.data_models.book import BookRecommedation


ai_controller_router = InferringRouter(prefix="/ai", tags=["AI"])

@ai_controller_router.get("/book/{book_name}", response_model=BookRecommedation)
async def get_author(book_name: str):
    books = BookAI().recommend_books_with_score(book_name)

    if books is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book does not exist")

    recommend = BookRecommedation.from_list(books)

    if recommend is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No results")

    return recommend

