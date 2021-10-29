from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi import Body
from fastapi import Path

# Cryptography
from cryptography.fernet import Fernet

# Database
from config.db import connection

# Models
from models.user import User

# Schemas
from schemas.user import CreateUser
from schemas.user import UserOut

# Utils
from config.settings import SECRET_KEY


router = APIRouter()


@router.post('/signup',
             response_model=UserOut,
             status_code=status.HTTP_201_CREATED,
             summary='Sign up',
             tags=['Auth', 'Users'])
def signup(user: CreateUser = Body(...)):
    """Sign up route.

    This path operation registers a new user in the app.

    Parameters:
    - Request body parameters:
        - **user: UserRegister**

    Returns a json object with the information of the registered user.
    - id: **int**
    - email: **EmailStr**
    - first_name: **str**
    - last_name: **str**
    - birth_date: **Optional[date]**
    - created_at: **datetime**
    - updated_at: **datetime**
    """

    user_dict = user.dict()
    user_dict['password'] = Fernet(SECRET_KEY).encrypt(user_dict['password'].encode('utf-8')).decode('utf-8')

    response = connection.execute(User.insert().values(**user_dict))

    user_dict['id'] = response.lastrowid
    user_dict['birth_date'] = str(user_dict['birth_date'])
    user_dict['created_at'] = str(datetime.utcnow())
    user_dict['updated_at'] = user_dict['created_at']

    return user_dict


# @router.post('/login',
#           response_model=UserLogin,
#           status_code=status.HTTP_200_OK,
#           summary='Login',
#           tags=['Auth', 'Users'])
# def login(user: User) -> User:
#     pass
