from src.data_models.book import BookIdModel
import src.auth as auth
from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from src.services.user_service import UserService
from src.data_models.user import FullUserModel, PublicUser, TokenData, TokenPair
from fastapi_utils.inferring_router import InferringRouter

user_controller_router = InferringRouter(prefix="/users", tags=["User"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
user_service = UserService()

def get_user_service() -> UserService:
    return user_service

async def authenticate_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    token_data = auth.decrypt_token(token)
    if (token_data is None or
            token_data.token_type != auth.ACCESS_KEY_TYPE_KEY):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return token_data

async def authenticate_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    token_data = auth.decrypt_token(token)
    if (token_data is None or
            token_data.token_type != auth.REFRESH_KEY_TYPE_KEY):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return token_data


@user_controller_router.post("/register")
async def register(user: FullUserModel, service = Depends(get_user_service)):
    usr = service.register(user)

    if usr:
        return JSONResponse({"msg": "Success"})
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

@user_controller_router.post("/login", response_model=TokenPair)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), service = Depends(get_user_service)):
    if not service.authenticate_by_password(form_data.username, form_data.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Icorrect username or password")

    access_token = service.create_access_token(form_data.username)
    refresh_token = service.create_refresh_token(form_data.username)
    service.add_refresh_token(refresh_token)

    return TokenPair(
        access_token = access_token.token_str,
        refresh_token = refresh_token.token_str
    )

'''
private route
needs refresh token
'''
@user_controller_router.get("/token", response_model=TokenPair)
async def refresh_token(token_data: Annotated[TokenData, Depends(authenticate_refresh_token)], service = Depends(get_user_service)):
    service.invalidate_refresh_token(token_data)
    access_token = service.create_access_token(token_data.username)
    refresh_token = service.create_refresh_token(token_data.username)

    return TokenPair(
        access_token = access_token.token_str,
        refresh_token = refresh_token.token_str
    )

'''
private route
needs access token
'''
@user_controller_router.get("", response_model=PublicUser)
async def get_user(token_data: Annotated[TokenData, Depends(authenticate_access_token)], service = Depends(get_user_service)):
    return service.get_user(token_data.username)

'''
private route
needs access token
'''
@user_controller_router.post("/books/like")
async def like_book(book_id: BookIdModel,  token_data: Annotated[TokenData, Depends(authenticate_access_token)], service = Depends(get_user_service)):
    if service.like_book(token_data.username, book_id.id):
        return JSONResponse({"msg": "Success"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

'''
private route
needs access token
'''
@user_controller_router.get("/books", response_model=list[BookIdModel])
async def get_books(token_data: Annotated[TokenData, Depends(authenticate_access_token)], service = Depends(get_user_service)):
    return service.get_liked_books(token_data.username)


'''
private route call example
'''
# token = "token"
# rs = rq.post("http://localhost:8000/users/token", headers={
#     "Authorization": "Bearer " + token
# })
#
# print(auth.decrypt_token(token))
# print(rs.status_code)
# print(rs.text)
