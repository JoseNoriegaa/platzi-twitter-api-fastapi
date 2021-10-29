# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from schemas.user import UserOut


class JWTAccessToken(BaseModel):
    access_token: str

    access_token_expiration: int


class JWTRefreshToken(BaseModel):

    refresh_token: str

    refresh_token_expiration: int


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
