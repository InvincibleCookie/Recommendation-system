from src.ai.book import BookAI

def test_table():
    ai = BookAI()
    assert ai.recommend_books_with_score('Fahrenheit 451') is not None
    assert ai.recommend_books_with_score('not a real book') is None

