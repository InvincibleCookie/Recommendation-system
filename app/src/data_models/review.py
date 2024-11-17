from datetime import datetime
from pydantic import BaseModel

class ReviewIdModel(BaseModel):
    id: int

class ReviewNoIdModel(BaseModel):
    title: str
    price: float
    username: str
    helpfulness: float
    score: float
    date: datetime
    summary: str
    review_text: str
    is_internal_user: bool
    book_id: int

class NewReviewModel(BaseModel):
    title: str
    price: float
    helpfulness: float
    score: float
    date: datetime
    summary: str
    review_text: str
    is_internal_user: bool
    book_id: int

    def to_no_id_model(self, username):
        return ReviewNoIdModel(
            username=username,
            title=self.title,
            price=self.price,
            helpfulness=self.helpfulness,
            score=self.score,
            date=self.date,
            summary=self.summary,
            review_text=self.review_text,
            is_internal_user=self.is_internal_user,
            book_id=self.book_id,
        )

class FullReviewModel(ReviewIdModel, ReviewNoIdModel):
     pass

class ReviewFilterModel(BaseModel):
    book_id: int | None
    ascendingSort: bool | None
    sortBy: str | None
