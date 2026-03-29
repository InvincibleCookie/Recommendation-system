# Recommendation System

Backend recommendation system for books built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and a simple **content-based recommendation engine** based on TF-IDF similarity over book tags.

## Overview

This project is a backend service for working with a book catalog, authors, genres, reviews, users, and personalized recommendations.

The system provides:

- user registration and JWT-based authentication;
- access and refresh tokens;
- book catalog browsing with filtering and sorting;
- author and genre lookup;
- review creation and retrieval;
- liked books management;
- AI-based book recommendations:
  - recommendations for a specific book;
  - recommendations based on all books liked by a user.

The application is exposed as a FastAPI service and can be started together with PostgreSQL through Docker Compose.

## Tech Stack

- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **JWT**
- **bcrypt**
- **pandas**
- **scikit-learn**
- **Docker Compose**

## Project Structure

```text
Recommendation-system/
├── app/
│   ├── main.py
│   ├── src/
│   │   ├── ai/
│   │   │   ├── book.py
│   │   │   └── data/
│   │   ├── common/
│   │   │   └── sigleton.py
│   │   ├── controllers/
│   │   │   ├── ai_controller.py
│   │   │   ├── author_controller.py
│   │   │   ├── book_controller.py
│   │   │   ├── common.py
│   │   │   ├── genre_controller.py
│   │   │   ├── review_controller.py
│   │   │   └── user_controller.py
│   │   ├── data_models/
│   │   │   ├── author.py
│   │   │   ├── book.py
│   │   │   ├── genres.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── database/
│   │   │   ├── postgres_association_tables.py
│   │   │   ├── postgres_author_table.py
│   │   │   ├── postgres_book_table.py
│   │   │   ├── postgres_db.py
│   │   │   ├── postgres_genre_table.py
│   │   │   ├── postgres_review_table.py
│   │   │   ├── postgres_token_table.py
│   │   │   └── postgres_user_table.py
│   │   ├── repositories/
│   │   │   ├── author_repository.py
│   │   │   ├── book_repository.py
│   │   │   ├── genre_repository.py
│   │   │   ├── review_repository.py
│   │   │   ├── user_repository.py
│   │   │   └── postgres/
│   │   │       ├── postgres_author_repository.py
│   │   │       ├── postgres_book_repository.py
│   │   │       ├── postgres_genre_repository.py
│   │   │       ├── postgres_review_repository.py
│   │   │       └── postgres_user_repository.py
│   │   ├── services/
│   │   │   ├── author_service.py
│   │   │   ├── book_service.py
│   │   │   ├── genre_service.py
│   │   │   ├── review_service.py
│   │   │   └── user_service.py
│   │   └── auth.py
│   └── tests/
├── datasets/
│   ├── Parse_tags.ipynb
│   ├── book-tags.ipynb
│   ├── daatset_best_reviews.ipynb
│   ├── dataset_preparation.ipynb
│   └── testing_dataset.ipynb
├── models/
│   ├── BookRecommendationModel.ipynb
│   ├── Book_classification.ipynb
│   ├── NewRecommSystem.ipynb
│   └── book_meta_with_tags.csv
├── .env.template
├── clean_docker.sh
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## Architecture

The project follows a layered architecture with clear separation of concerns:

- **Controllers** — define API endpoints and handle HTTP requests/responses.
- **Services** — contain business logic and coordinate data flow.
- **Repositories** — abstract database access and queries.
- **Database models** — SQLAlchemy ORM models describing PostgreSQL tables.
- **Data models** — Pydantic schemas for validation and serialization.
- **AI module** — handles recommendation logic using TF-IDF.

This structure makes the system scalable, testable, and easy to extend.

---

## Features

### Authentication and Users

- User registration (username, email, password)
- JWT-based authentication
- Access and refresh tokens
- Token refresh mechanism
- Get current user profile
- Like/unlike books
- Retrieve liked books

**Security details:**

- Passwords are hashed using `bcrypt`
- JWT payload includes:
  - `username`
  - `token_id`
  - `type`
  - `exp`

**Token lifetime:**

- Access token: 24 hours
- Refresh token: 30 days

---

### Books

Supports:

- Retrieve a book by ID
- List books with filters and sorting
- Pagination via `offset` and `itemCount`

**Filters:**

- Title pattern
- Authors
- Genres
- Publish date range
- Rating range

**Sorting fields:**

- `title`
- `publishdate`
- `raiting`
- `popularity`

---

### Authors

Supports:

- Get author by ID
- List authors
- Filter by name pattern
- Sort by name
- Pagination

---

### Genres

Supports:

- Get genre by ID
- List genres
- Filter by name pattern
- Sort by name
- Pagination

---

### Reviews

Supports:

- Add review
- Get review by ID
- List reviews
- Filter by book
- Sort by score, date, helpfulness

Reviews can be:

- Internal (linked to registered user)
- External (stored as foreign user data)

---

### Recommendation Engine

Located in: `app/src/ai/book.py`

**Core approach:** Content-based filtering using TF-IDF.

**Pipeline:**

1. Load dataset (`book_meta_with_tags.csv`)
2. Combine tag-related fields into a single text representation
3. Compute TF-IDF vectors
4. Calculate cosine similarity
5. Adjust scores using book rating
6. Return top-N similar books

**Supported modes:**

- Recommendations for a single book
- Recommendations based on user's liked books

---

## Database Schema

The database is automatically initialized if not present.

### Main Tables

#### `user_data`

- `id`
- `email` (unique)
- `username` (unique)
- `password_hash`

Relations:

- One-to-many with tokens
- Many-to-many with liked books
- One-to-many with reviews

---

#### `user_token`

- `id`
- `user_id`
- `token_id`
- `expiry_date`

---

#### `book_data`

- `id`
- `title`
- `description`
- `publisher`
- `publishDate`
- `coverLink`
- `raiting`
- `popularity`

Relations:

- Many-to-many with authors
- Many-to-many with genres
- One-to-many with reviews

---

#### `author`

- `id`
- `name` (unique)

---

#### `genre`

- `id`
- `name` (unique)

---

#### `review_data`

- `id`
- `title`
- `price`
- `helpfulness`
- `score`
- `date`
- `summary`
- `review_text`
- `book_id`
- `foreign_user_id`
- `foreign_username`
- `is_internal_user`
- `internal_user_id`

---

### Association Tables

- `book_to_genre_association`
- `book_to_author_association`
- `book_to_user_like_association`

---

## Environment Variables

Create a `.env` file based on `.env.template`.

```env
POSTGRES_PASSWORD=<password>
POSTGRES_USER=<user>
POSTGRES_HOST=<db_host>
POSTGRES_PORT=<port>
DB_NAME=<name>
MAIN_SERVER_PORT=<port>
MAIN_SERVER_HOST=<host>
JWT_SECRET_KEY=<key>
```

Example:

```env
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
POSTGRES_HOST=dataBase
POSTGRES_PORT=5432
DB_NAME=recommendation_db
MAIN_SERVER_PORT=8000
MAIN_SERVER_HOST=0.0.0.0
JWT_SECRET_KEY=super_secret_key
```

## Installation
### Option 1. Run with Docker Compose
1. Clone the repository:
   ```bash
   git clone https://github.com/InvincibleCookie/Recommendation-system.git
   cd Recommendation-system
   ```
2. Create .env from template:
  ```bash
  cp .env.template .env
  ```
3. Fill in environment variables.
4. Run the project:
   ```bash
   docker compose up --build
    ```
The stack starts:
* PostgreSQL
* FastAPI application

### Option 2. Run locally
1. Clone the repository:
   ```bash
   git clone https://github.com/InvincibleCookie/Recommendation-system.git
   cd Recommendation-system
   ```
2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
    ```
   On Windows:
   ```bash
   .venv\Scripts\activate
    ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create ```.env``` file from ```.env.template```.
5. Make sure PostgreSQL is running and accessible.
6. Start the server:
   ```bash
   python app/main.py
   ```


   
