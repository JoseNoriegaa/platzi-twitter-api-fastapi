from typing import List
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi import Response
from fastapi import Body
from fastapi import Path
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

# Database
from config.db import connection

# Middlewares
from middleware.auth import get_current_user

# Models
from models.user import User

# Schemas
from schemas.user import CreateUser
from schemas.user import UserOut
from schemas.user import User as UserSchema

# Utils
from utils.passwords import hash_password


router = APIRouter()


@router.get('/users/',
         response_model=List[UserOut],
         status_code=status.HTTP_200_OK,
         summary='Get all users',
         tags=['Users'])
def list_users():
    """List all users.

    This path operation shows all users in the app.

    Returns a json object with the information of all users.
    - id: **int**
    - first_name: **str**
    - last_name: **str**
    - email: **EmailStr**
    - created_at: **datetime**
    - updated_at: **datetime**
    """

    response = connection.execute(User.select()).fetchall()

    return response


@router.get('/users/{id}',
         response_model=UserOut,
         status_code=status.HTTP_200_OK,
         summary='Get a user',
         tags=['Users'])
def retrieve_user(
    id: int = Path(...,
                   gt=0,
                   title='User ID',
                   description='ID of the user to retrieve'),
):
    """Retrieve user.

    This path operation allows to get the information of a specific user.

    Parameters:
    - Path parameters:
        - id: **int**

    Returns a json object with the information of the user.
    - id: **int**
    - first_name: **str**
    - last_name: **str**
    - email: **EmailStr**
    - created_at: **datetime**
    - updated_at: **datetime**
    """

    response = connection.execute(User.select().where(User.c.id == id)).fetchone()

    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    return response


@router.put('/users/{id}',
         response_model=UserOut,
         status_code=status.HTTP_200_OK,
         summary='Update user',
         tags=['Users'])
def update_user(
    id: int = Path(...,
                   gt=0,
                   title='User ID',
                   description='ID of the user to update'),
    user: CreateUser = Body(...,),
    request_user: UserSchema = Depends(get_current_user),
):
    """Update user.

    This operation path updates the information of a specific user.

    Users can only update their own information.

    Parameters:
    - Path parameters:
        - id: **str**

    - Body parameters:
        - user: **CreateUser**

    Returns the information of the updated user.
    - id: **int**
    - first_name: **str**
    - last_name: **str**
    - email: **EmailStr**
    - created_at: **datetime**
    - updated_at: **datetime**
    """

    user_response = connection.execute(User.select().where(User.c.id == id)).fetchone()

    if user_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    if user_response.id != request_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')

    # Update user
    updated_user = {
        **user_response,
        **user.dict(),
    }

    updated_user['password'] = hash_password(updated_user['password'])

    # Save user
    try:
        connection.execute(User.update(User.c.id == id).values(**updated_user))
    except IntegrityError as e:
        str_error = str(e)
        if 'Duplicate entry' in str_error and 'users.email' in str_error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email already registered.') from e

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error.') from e

    updated_user['updated_at'] = str(datetime.now())

    return updated_user


@router.delete('/users/{id}',
               status_code=status.HTTP_204_NO_CONTENT,
               summary='Delete user',
               tags=['Users'])
def delete_user(
    id: int = Path(...,
                   gt=0,
                   title='User ID',
                   description='ID of the user to delete'),
    request_user: UserSchema = Depends(get_current_user),
):
    """Delete user.

    This path operation deletes a specific user in the app.

    Users can only delete their own information.

    Parameters:
    - Path parameters:
        - id: **str**
    """

    user_response = connection.execute(User.select().where(User.c.id == id)).fetchone()

    if user_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    if user_response.id != request_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')

    # Delete user
    connection.execute(User.delete().where(User.c.id == id))

    return Response(status_code=status.HTTP_204_NO_CONTENT)
