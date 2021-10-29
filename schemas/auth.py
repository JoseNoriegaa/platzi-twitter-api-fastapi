# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from schemas.user import UserOut


class BaseJWTAccessToken(BaseModel):
    access_token: str = Field(...,
                              min_length=8,
                              example='access_token',)


class JWTAccessToken(BaseJWTAccessToken):
    access_token_expiration: int = Field(...,
                                         gt=0,
                                         example=60,
                                         description='Access token expiration in seconds')


class BaseJWTRefreshToken(BaseModel):
    refresh_token: str = Field(...,
                               min_length=8,
                               example='refresh_token',)


class JWTRefreshToken(BaseJWTRefreshToken):

    refresh_token_expiration: int = Field(...,
                                          gt=0,
                                          example=60,
                                          description='Refresh token expiration in seconds')


class JWTCredentials(JWTAccessToken, JWTRefreshToken):
    pass


class LoginRequest(BaseModel):
    email: EmailStr = Field(...,)

    password: str = Field(...,
                        min_length=8,
                        max_length=255,
                        example='password',)


class LoginReponse(JWTCredentials):

    user: UserOut
