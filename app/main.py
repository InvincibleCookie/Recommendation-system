from fastapi import FastAPI
import uvicorn
from src.controllers.user_controller import user_controller_router
from src.controllers.book_controller import book_controller_router
from src.controllers.author_controller import author_controller_router
from src.controllers.genre_controller import genre_controller_router
import os

app = FastAPI()

app.include_router(user_controller_router, prefix="/user", tags=["User"])
app.include_router(book_controller_router, prefix="/book", tags=["Book"])
app.include_router(author_controller_router, prefix="/author", tags=["Author"])
app.include_router(genre_controller_router, prefix="/genre", tags=["Genre"])

if __name__ == '__main__':
    port = os.environ.get("MAIN_SERVER_PORT")
    host = os.environ.get("MAIN_SERVER_HOST")

    if  port is None or host is None:
        print("Bad environment")
        exit(1)

    uvicorn.run(app, host=host, port=int(port), root_path=".")

