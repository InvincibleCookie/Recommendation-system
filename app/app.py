from fastapi import FastAPI
import uvicorn
from controllers.user_controller import user_controller_router
import os

app = FastAPI()

app.include_router(user_controller_router, prefix="/user", tags=["User"])

if __name__ == '__main__':
    port = os.environ.get("MAIN_SERVER_PORT")
    host = os.environ.get("MAIN_SERVER_HOST")

    if  port is None or host is None:
        print(" Bad environment")
        exit(1)

    uvicorn.run("app:app",host=host, port=int(port))

