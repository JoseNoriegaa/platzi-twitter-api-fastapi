from typing import Dict
from typing import Any

# FastAPI
from fastapi import Request
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from fastapi import status

# Utilities
from config import settings
from utils.jsonwebtoken import verify_token

# Database
from config.db import connection

# Models
from models.user import User

# Schemas
from schemas.user import User as UserSchema


class JWTBearer(HTTPBearer):
    """
    JWT token Handler.
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail='Invalid authentication scheme.')

            return credentials.credentials

        raise HTTPException(status_code=403, detail='Invalid authorization code.')


def validate_acccess_token(token: str = Depends(JWTBearer())) -> Dict[str, Any]:
    """
    Validate access token.

    Args:
        token: JWT token.

    Returns:
        Dict[str, Any]: User data.
    """

    base_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail='Invalid credentials.',
                                   headers={'WWW-Authenticate': 'Bearer'})

    decoded_token = verify_token(token)

    if not decoded_token:
        raise base_exception

    if not decoded_token.get('type') == settings.JWT_ACCESS_TOKEN_TYPE:
        raise base_exception

    return decoded_token


def get_current_user(decoded_token: Dict[str, any] = Depends(validate_acccess_token)) -> User:
    """
    Get current user.
    """

    base_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail='Invalid credentials.',
                                   headers={'WWW-Authenticate': 'Bearer'})

    if not isinstance(decoded_token, dict) or not 'sub' in decoded_token:
        raise base_exception

    user = connection.execute(User.select().where(User.c.id == decoded_token.get('sub'))).fetchone()

    if not user:
        raise base_exception

    return UserSchema(**user)
