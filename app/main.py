import os
import uvicorn
from fastapi import FastAPI
from src.controllers.user_controller import user_controller_router
from src.controllers.book_controller import book_controller_router
from src.controllers.author_controller import author_controller_router
from src.controllers.genre_controller import genre_controller_router
from src.controllers.review_controller import review_controller_router
from src.controllers.ai_controller import ai_controller_router

app = FastAPI()

app.include_router(user_controller_router)
app.include_router(book_controller_router)
app.include_router(author_controller_router)
app.include_router(genre_controller_router)
app.include_router(review_controller_router)
app.include_router(ai_controller_router)

if __name__ == '__main__':
    port = os.environ.get("MAIN_SERVER_PORT")
    host = os.environ.get("MAIN_SERVER_HOST")

    if  port is None or host is None:
        print("Bad environment")
        exit(1)

    uvicorn.run(app, host=host, port=int(port), root_path=".")

