from typing import Annotated, Optional
import src.auth as auth
from src.data_models.user import TokenData
from src.services.user_service import UserService
from src.data_models.review import FullReviewModel, NewReviewModel, ReviewFilterModel, ReviewIdModel
from src.services.review_service import ReviewService
from fastapi import Depends, HTTPException, Query, status
from fastapi_utils.inferring_router import InferringRouter
from .common import get_array_window

review_controller_router = InferringRouter(prefix="/reviews", tags=["Review"])
review_service = ReviewService()
user_service = UserService()

def get_review_service() -> ReviewService:
    return review_service

def get_user_service() -> UserService:
    return user_service

'''
private route
needs access token
'''
@review_controller_router.post("/add", response_model=ReviewIdModel)
async def add_review(
    review: NewReviewModel,
    token_data: Annotated[TokenData, Depends(auth.authenticate_access_token)],
    user_service: UserService = Depends(get_user_service),
    review_service: ReviewService = Depends(get_review_service),
):
    user = user_service.get_internal_user(token_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    review_id = review_service.add_review(review.to_no_id_model(user.username), user.id)
    if review_id == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create review")

    return ReviewIdModel(id = review_id)

@review_controller_router.get("/{review_id}", response_model=FullReviewModel)
async def get_review(review_id: int, service: ReviewService = Depends(get_review_service)):
    book = service.get_review(review_id)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review does not exist")

    return book

@review_controller_router.get("", response_model=list[FullReviewModel])
async def get_reviews(
    book_id: Optional[int] = Query(None, description="Filter by book id"),
    ascendingSort: Optional[bool] = Query(None, description="Sort in ascending order"),
    sortBy: Optional[str] = Query(None, description="Sort by parameter"),
    offset: Optional[int] = Query(None, description="Number of items that will be skipped in the returned array"),
    itemCount: Optional[int] = Query(None, description="Max number of items to be returned"),
    service = Depends(get_review_service)
):
    filt = ReviewFilterModel(
        book_id=book_id,
        sortBy=sortBy,
        ascendingSort=ascendingSort,
    )

    reviews = service.get_books_by_filter(filt)
    if offset is None:
        offset = 0

    if itemCount == None:
        itemCount = len(reviews)

    return get_array_window(reviews, offset, itemCount)

