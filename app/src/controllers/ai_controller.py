from fastapi import Depends, HTTPException, Query, status
from fastapi_utils.inferring_router import InferringRouter
from src.services.book_service import BookService
from typing import Annotated
from src.data_models.user import FullUserModel, PublicUser, TokenData, TokenPair
import src.auth as auth
import random

from src.services.user_service import UserService
from src.ai.book import BookAI
from src.data_models.book import BookRecommedation, BookModel, BookIdModel

user_service = UserService()

def get_user_service() -> UserService:
    return user_service

ai_controller_router = InferringRouter(prefix="/ai", tags=["AI"])
book_service = BookService()

def get_book_service() -> BookService:
    return book_service



'''
private route
needs access token
'''
@ai_controller_router.get("/book/all", response_model=BookRecommedation)
async def get_recommend_all(token_data: Annotated[TokenData, Depends(auth.authenticate_access_token)],
                            user_service: UserService = Depends(get_user_service),
                            book_service: BookService = Depends(get_book_service)):
    book_ls: list[BookIdModel] = user_service.get_liked_books(token_data.username)
    books_recommend = []

    for i in book_ls:
        book = book_service.get_book(i.id)
        if book is None:
            continue

        new_rec = BookAI().recommend_books_with_score(book.title)
        if new_rec is None:
            continue

        books_recommend.extend(new_rec)

    random.shuffle(books_recommend)

    recommend = BookRecommedation.from_list(books_recommend)

    if recommend is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No results")

    return recommend

@ai_controller_router.get("/book/{book_id}", response_model=BookRecommedation)
async def get_recommend(book_id: int, service = Depends(get_book_service)):
    book: BookModel = service.get_book(book_id)

    books = BookAI().recommend_books_with_score(book.title)

    if books is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book does not exist")

    recommend = BookRecommedation.from_list(books)

    if recommend is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No results")

    return recommend
