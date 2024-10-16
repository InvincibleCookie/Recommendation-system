import auth
from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from services.user_service import UserService
from fastapi_utils.cbv import cbv
from data_models.user import FullUserModel, PublicUser, TokenData, TokenPair
from fastapi_utils.inferring_router import InferringRouter

user_controller_router = InferringRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

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

@cbv(user_controller_router)
class UserController:
    def __init__(self):
        self.userService = UserService()

    @user_controller_router.post("/register")
    async def register(self, user: FullUserModel):
        usr = self.userService.register(user)

        if usr:
            return JSONResponse({"msg": "Success"})
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    @user_controller_router.post("/login", response_model=TokenPair)
    async def get_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        if not self.userService.authenticate_by_password(form_data.username, form_data.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Icorrect username or password")

        access_token = self.userService.create_access_token(form_data.username)
        refresh_token = self.userService.create_refresh_token(form_data.username)
        self.userService.add_refresh_token(refresh_token)

        return TokenPair(
            access_token = access_token.token_str,
            refresh_token = refresh_token.token_str
        )

    '''
    private method
    needs refresh token
    '''
    @user_controller_router.post("/token", response_model=TokenPair)
    async def refresh_token(self, token_data: Annotated[TokenData, Depends(authenticate_refresh_token)]):
        self.userService.invalidate_refresh_token(token_data)
        access_token = self.userService.create_access_token(token_data.username)
        refresh_token = self.userService.create_refresh_token(token_data.username)

        return TokenPair(
            access_token = access_token.token_str,
            refresh_token = refresh_token.token_str
        )

    '''
    private method
    needs access token
    '''
    @user_controller_router.post("/get", response_model=PublicUser)
    async def get_user(self, token_data: Annotated[TokenData, Depends(authenticate_access_token)]):
        return self.userService.get_user(token_data.username)


'''
private method call example
'''
# token = "token"
# rs = rq.post("http://localhost:8000/users/token", headers={
#     "Authorization": "Bearer " + token
# })
#
# print(auth.decrypt_token(token))
# print(rs.status_code)
# print(rs.text)
