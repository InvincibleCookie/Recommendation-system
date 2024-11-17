from src.data_models.review import FullReviewModel, ReviewFilterModel, ReviewNoIdModel
from src.repositories.postgres.postgres_review_repository import PostgresReviewRepository

class ReviewService:
    def __init__(self):
        self.repository = PostgresReviewRepository()

    def add_review(self, review: ReviewNoIdModel, user_id: int) -> int:
        return self.repository.add_review(review, user_id, review.is_internal_user)

    def get_review(self, review_id: int) -> FullReviewModel | None:
        return self.repository.get_review(review_id)

    def get_reviews_by_filter(self, filt: ReviewFilterModel) -> list[FullReviewModel]:
        return self.repository.get_reviews_by_filter(filt)
