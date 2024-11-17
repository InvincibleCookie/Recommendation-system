from sqlalchemy import select
from typing import Tuple
from sqlalchemy.sql.selectable import Select
from sqlalchemy.orm import Session
from src.data_models.review import FullReviewModel, ReviewFilterModel, ReviewNoIdModel
from src.database.postgres_review_table import ReviewInDB
from src.repositories.review_repository import ReviewRepository
from src.database.postgres_db import PostgresDB

def db_to_model(review: ReviewInDB):
    return FullReviewModel(
        id = review.id,
        title = review.title,
        price = review.price,
        username = review.internal_user.username if review.is_internal_user else review.foreign_username,
        helpfulness = review.helpfulness,
        score = review.score,
        date = review.date,
        summary = review.summary,
        review_text = review.review_text,
        is_internal_user = review.is_internal_user,
        book_id = review.book_id,
    )

def model_to_db(review: ReviewNoIdModel, user_id: int, internal: bool):
    return ReviewInDB(
        title = review.title,
        price = review.price,
        foreign_user_id = user_id if not internal else None,
        internal_user_id = user_id if internal else None,
        foreign_username = review.username if not internal else None,
        helpfulness = review.helpfulness,
        score = review.score,
        date = review.date,
        summary = review.summary,
        review_text = review.review_text,
        is_internal_user = internal,
        book_id = review.book_id,
    )

class PostgresReviewRepository(ReviewRepository):

    def _get_engine(self):
        return PostgresDB().get_engine()

    def add_review(self, review_model: ReviewNoIdModel, user_id: int, internal: bool) -> int:
        with Session(self._get_engine()) as session:
            try:
                review = model_to_db(review_model, user_id, internal)
                session.add(review)
                session.commit()

                return review.id
            except:
                return -1


    def get_review(self, review_id: int) -> FullReviewModel | None:
        with Session(self._get_engine()) as session:
            try:
                return db_to_model(session.get_one(ReviewInDB, review_id))
            except:
                return None

    def add_sort(self, filt: ReviewFilterModel, stmt: Select[Tuple[ReviewInDB]]) -> Select[Tuple[ReviewInDB]]:
        if filt.sortBy is None:
            return stmt

        col = None

        match filt.sortBy:
            case "score": col = ReviewInDB.score
            case "date": col = ReviewInDB.date
            case "helpfullness": col = ReviewInDB.helpfulness
            case _: return stmt

        if filt.ascendingSort or filt.ascendingSort is None:
            return stmt.order_by(col.asc())

        return stmt.order_by(col.desc())

    def get_reviews_by_filter(self, filt: ReviewFilterModel) -> list[FullReviewModel]:
        with Session(self._get_engine()) as session:
            try:
                stmt = select(ReviewInDB)

                if filt.book_id is not None:
                    stmt = stmt.where(ReviewInDB.book_id == filt.book_id)

                stmt = self.add_sort(filt, stmt)

                reviews = session.scalars(stmt)

                ls = []

                for i in reviews:
                    ls.append(db_to_model(i))

                return ls
            except:
                return []

