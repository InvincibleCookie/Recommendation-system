from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from src.common.sigleton import Singleton

DATA_FILE = 'app/src/ai/data/book_meta_with_tags.csv'

class BookAI(metaclass=Singleton):
    def __init__(self) -> None:
        data = pd.read_csv(DATA_FILE)
        df = data.copy()

        df = df[['Title', 'authors', 'categories', 'avgScore', 'Genres', 'Themes', 'Settings',
                'Tone/Mood', 'Audience','Writing Style', 'Features', 'Time Period', 'image']]

        selected_columns = ['categories', 'Genres', 'Themes', 'Settings',
            'Tone/Mood', 'Audience','Writing Style', 'Features', 'Time Period']

        df_cleaned = df[~df[selected_columns].isnull().all(axis=1)]

        columns_to_merge = [
            'categories', 'Genres', 'Themes', 'Settings', 'Tone/Mood',
            'Audience', 'Writing Style', 'Features', 'Time Period'
        ]

        def merge_tags(row):
            tags = []
            for value in row:
                if isinstance(value, list):  # Если значение — список, преобразуем его в строку
                    tags.append(' '.join(value))
                elif pd.notnull(value):  # Если значение не NaN, добавляем его как есть
                    tags.append(str(value))
            return ', '.join(tags).replace('[', '').replace(']', '').replace("'", "")


        df['tags'] = df[columns_to_merge].apply(merge_tags, axis=1)
        tags_split = df['tags'].head(1).iloc[0].split(', ')

        self.df = df.dropna(subset=['tags'])

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['tags'])

        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.book_indices = pd.Series(df.index, index=df['Title']).drop_duplicates()

    def recommend_books_with_score(self, title, weight=0.3) -> None | list[list[str]]:
        """
        Рекомендации с учетом среднего рейтинга книг.

        :param title: Название книги, для которой ищем рекомендации.
        :param cosine_sim: Матрица косинусного сходства.
        :param df: DataFrame с данными о книгах.
        :param weight: Влияние avgScore на итоговый результат (0.0–1.0).
        :return: DataFrame с рекомендованными книгами.
        """
        # Проверяем наличие книги
        if title not in self.df['Title'].values:
            return None

        # Индекс книги
        idx = self.df.index[self.df['Title'] == title][0]

        # Сходство книги с другими
        sim_scores = list(enumerate(self.cosine_sim[idx]))

        # Добавляем влияние avgScore
        for i, _ in enumerate(sim_scores):
            sim_scores[i] = (sim_scores[i][0], sim_scores[i][1] + weight * self.df.iloc[sim_scores[i][0]]['avgScore'])

        # Сортируем по убыванию результата
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Берем топ-5 книг (кроме самой первой, так как это текущая книга)
        sim_scores = sim_scores[1:6]

        # Получаем индексы рекомендованных книг
        recommended_indices = [i[0] for i in sim_scores]

        # Возвращаем DataFrame с рекомендациями
        return self.df.iloc[recommended_indices][['Title', 'authors', 'image']].values
