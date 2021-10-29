from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi import Body
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

# Database
from config.db import connection

# Models
from models.user import User

# Schemas
from schemas.user import CreateUser
from schemas.user import UserOut
from schemas.auth import LoginRequest
from schemas.auth import LoginReponse
from schemas.auth import BaseJWTRefreshToken
from schemas.auth import JWTAccessToken

# Utils
from utils.passwords import hash_password
from utils.passwords import check_password
from utils.jsonwebtoken import create_credentials
from utils.jsonwebtoken import create_access_token
from utils.jsonwebtoken import verify_token
from utils.user import get_fullname


router = APIRouter()


@router.post('/signup',
             response_model=LoginReponse,
             status_code=status.HTTP_201_CREATED,
             summary='Sign up',
             tags=['Auth', 'Users'])
def signup(user: CreateUser = Body(...)):
    """Sign up route.

    This path operation registers a new user in the app.

    Parameters:
    - Request body parameters:
        - user: **UserRegister**

    Returns a json object with the information of the registered user and its credentials.
    - user: **UserOut**
    - access_token: **str**
    - access_token_expiration: **int**
    - refresh_token: **str**
    - refresh_token_expiration: **int**
    """

    user_dict = user.dict()
    user_dict['password'] = hash_password(user_dict['password'])

    try:
        response = connection.execute(User.insert().values(**user_dict))
    except IntegrityError as e:
        str_error = str(e)
        if 'Duplicate entry' in str_error and 'users.email' in str_error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email already registered.') from e

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error.') from e

    user_dict['id'] = response.lastrowid
    user_dict['birth_date'] = str(user_dict['birth_date'])
    user_dict['created_at'] = str(datetime.utcnow())
    user_dict['updated_at'] = user_dict['created_at']

    response = {
        'user': user_dict,
    }
    response.update(create_credentials(response['user']))

    return response


@router.post('/login',
          response_model=LoginReponse,
          status_code=status.HTTP_200_OK,
          summary='Login',
          tags=['Auth', 'Users'])
def login(user: LoginRequest = Body(...)):
    """Login route.

    This operation path allows a user to login in the app.

    Parameters:
    - Request body parameters:
        - user: **LoginRequest**

    Returns a json object with the information of the logged user.
    - user: **UserOut**
    - access_token: **str**
    - access_token_expiration: **int**
    - refresh_token: **str**
    - refresh_token_expiration: **int**
    """

    registed_user = connection.execute(User.select().where(User.c.email == user.email)).fetchone()

    if registed_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')


    password_match = check_password(user.password, registed_user.password)

    if not password_match:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials')

    response = {
        'user': UserOut(**registed_user),
    }
    response.update(create_credentials(response['user']))

    return response


@router.post('/refresh',
             response_model=JWTAccessToken,
             status_code=status.HTTP_200_OK,
             summary='Refresh token',
             tags=['Auth', 'Users'])
def refresh_token(refresh_token: BaseJWTRefreshToken = Body(...)):
    """Refresh token route.

    This operation path allows a user to refresh the access token.

    Parameters:
    - Request body parameters:
        - refresh_token: **BaseJWTRefreshToken**

    Returns a json object with the new access token information.
    - access_token: **str**
    - access_token_expiration: **int**
    """

    decoded_token = verify_token(refresh_token.refresh_token)

    base_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid token')

    if decoded_token is None:
        raise base_exception

    user = connection.execute(User.select().where(User.c.id == decoded_token['sub'])).fetchone()

    if user is None:
        raise base_exception

    token, expiration = create_access_token({
        'sub': user.id,
        'email': user.email,
        'name': get_fullname(user),
    })

    response = {
        'access_token': token,
        'access_token_expiration': expiration,
    }

    return response
