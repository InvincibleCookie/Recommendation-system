from abc import abstractmethod

from src.data_models.review import FullReviewModel, ReviewFilterModel, ReviewNoIdModel


class ReviewRepository:
    @abstractmethod
    def add_review(self, review_model: ReviewNoIdModel, user_id: int, internal: bool) -> int: pass

    @abstractmethod
    def get_review(self, review_id: int) -> FullReviewModel | None: pass

    @abstractmethod
    def get_reviews_by_filter(self, filt: ReviewFilterModel) -> list[FullReviewModel]: pass
