"""
Author: Jose Noriega <josenoriega723@gmail.com>
Description: A simple Twitter API for learning purposes.
Last Update: 2021-10-27
"""

# Python
import json
import os
from uuid import UUID
from uuid import uuid4
from datetime import date
from datetime import datetime
from typing import List
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Path
from fastapi import Body
from fastapi import HTTPException
from fastapi import Response


# Settings
USERS_FILE = 'users.json'
USERS_STORAGE = os.path.join(os.path.dirname(__file__), USERS_FILE)

TWEETS_FILE = 'tweets.json'
TWEETS_STORAGE = os.path.join(os.path.dirname(__file__), TWEETS_FILE)

# Initialize the app
app = FastAPI()


# ============================================================
# Define models
# ============================================================


class IDMixin(BaseModel):
    id: UUID =  Field(..., title='User ID')


class TimeStampsMixin(BaseModel):
    created_at: datetime = Field(default=datetime.now(),
                                title='Creation date',
                                example='2020-01-01T00:00:00Z',)

    updated_at: Optional[datetime] = Field(default=None,
                                           title='Last update date',
                                           example='2020-01-01T00:00:00Z',)


class UserBase(BaseModel):

    email: EmailStr = Field(...,)


class UserProfile(UserBase):
    first_name: str = Field(...,
                            title='First name',
                            min_length=2,
                            max_length=50,
                            example='John',)

    last_name: str = Field(...,
                           title='Last name',
                           min_length=2,
                           max_length=50,
                           example='Doe',)

    birth_date: Optional[date] = Field(default=None,
                                       title='Birth date',
                                       example='2021-01-01',)


class User(IDMixin, UserProfile, TimeStampsMixin, UserBase):
    pass


class PasswordMixin(BaseModel):
    password: str = Field(...,
                          min_length=8,
                          max_length=64,
                          example='password',)


class UserLogin(PasswordMixin, UserBase):
    pass


class UserRegister(PasswordMixin, UserProfile):
    pass


class BaseTweet(BaseModel):
    content: str = Field(...,
                        min_length=1,
                        max_length=256,)


class Tweet(IDMixin, TimeStampsMixin, BaseTweet):

    created_by: User = Field(...,
                             title='User who created the tweet',)


class RegisterTweet(BaseTweet):

    created_by: str = Field(...,
                            title='ID of the user who created the tweet',)


# ============================================================
# Path operations
# ============================================================


## Auth
@app.post('/auth/signup',
          response_model=User,
          status_code=status.HTTP_201_CREATED,
          summary='Sign up',
          tags=['Auth', 'Users'])
def signup(user: UserRegister = Body(...)) -> User:
    """Sign up route.

    This path operation registers a new user in the app.

    Parameters:
    - Request body parameters:
        - **user: UserRegister**

    Returns a json object with the information of the registered user.
    - **id: UUID**
    - **email: EmailStr**
    - **first_name: str**
    - **last_name: str**
    - **birth_date: Optional[date]**
    - **created_at: datetime**
    - **updated_at: Optional[datetime]**
    """

    user_dict = {
        'id': str(uuid4()),
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birth_date': str(user.birth_date),
        'created_at': str(datetime.now()),
        'updated_at': None,
    }

    with open(USERS_STORAGE, 'w+', encoding='utf-8') as f:
        if os.path.exists(USERS_STORAGE):
            try:
                results = json.load(f)
                f.seek(0)
                f.truncate()
            except json.JSONDecodeError:
                results = []
        else:
            results = []

        results.append(user_dict)
        f.write(json.dumps(results))

    return user_dict


@app.post('/auth/login',
          response_model=UserLogin,
          status_code=status.HTTP_200_OK,
          summary='Login',
          tags=['Auth', 'Users'])
def login(user: User) -> User:
    pass


## Users


@app.get('/users/',
         response_model=List[User],
         status_code=status.HTTP_200_OK,
         summary='Get all users',
         tags=['Users'])
def list_users() -> List[User]:
    """List all users.

    This path operation shows all users in the app.

    Returns a json object with the information of all users.
    - **id: UUID**
    - **email: EmailStr**
    - **first_name: str**
    - **last_name: str**
    - **birth_date: Optional[date]**
    - **created_at: datetime**
    - **updated_at: Optional[datetime]**
    """

    if os.path.exists(USERS_STORAGE):
        with open(USERS_STORAGE, 'r', encoding='utf-8') as f:
            results = json.load(f)

    else:
        results = []

    return results


@app.get('/users/{id}',
         response_model=User,
         status_code=status.HTTP_200_OK,
         summary='Get a user',
         tags=['Users'])
def retrieve_user(
    id: str = Path(...,
                   title='User ID',
                   description='ID of the user to retrieve'),
) -> User:
    """Retrieve user.

    This path operation allows to get the information of a specific user.

    Parameters:
    - Path parameters:
        - **id: str**

    Returns a json object with the information of the user.
    - **id: UUID**
    - **email: EmailStr**
    - **first_name: str**
    - **last_name: str**
    - **birth_date: Optional[date]**
    - **created_at: datetime**
    - **updated_at: Optional[datetime]**
    """

    if os.path.exists(USERS_STORAGE):
        with open(USERS_STORAGE, 'r', encoding='utf-8') as f:
            results = json.load(f)

        for user in results:
            if user['id'] == id:
                return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User not found')


@app.put('/users/{id}',
         response_model=User,
         status_code=status.HTTP_200_OK,
         summary='Update user',
         tags=['Users'])
def update_user(
    id: str = Path(...,
                   title='User ID',
                   description='ID of the user to update'),
    user: UserRegister = Body(...,)
) -> User:
    """Update user.

    This operation path updates the information of a specific user.

    Parameters:
    - Path parameters:
        - **id: str**

    - Body parameters:
        - **user: UserRegister**

    Returns the information of the updated user.
    - **id: UUID**
    - **email: EmailStr**
    - **first_name: str**
    - **last_name: str**
    - **birth_date: Optional[date]**
    - **created_at: datetime**
    - **updated_at: Optional[datetime]**
    """

    index = None

    if os.path.exists(USERS_STORAGE):
        with open(USERS_STORAGE, 'r+', encoding='utf-8') as f:
            users = json.load(f)


            for idx, raw_user in enumerate(users):
                if raw_user['id'] == id:
                    index = idx
                    break

            if index is not None:
                users[index].update({
                    **user.dict(),
                    'birth_date': str(user.birth_date),
                    'updated_at': str(datetime.now()),
                })

                f.seek(0)
                f.truncate()
                f.write(json.dumps(users))

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found.')

    return users[index]


@app.delete('/users/{id}',
            status_code=status.HTTP_204_NO_CONTENT,
            summary='Delete user',
            tags=['Users'])
def delete_user(
    id: str = Path(...,
                   title='User ID',
                   description='ID of the user to delete'),
) -> User:
    """Delete user.

    This path operation deletes a specific user in the app.

    Parameters:
    - Path parameters:
        - **id: str**
    """

    found = False

    if os.path.exists(USERS_STORAGE):
        with open(USERS_STORAGE, 'r+', encoding='utf-8') as f:
            raw_users = json.load(f)

            users = []

            for raw_user in raw_users:
                if raw_user['id'] == id:
                    found = True
                else:
                    users.append(raw_user)

            if found:
                f.seek(0)
                f.truncate()
                f.write(json.dumps(users))

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found.')

    return Response(status_code=status.HTTP_204_NO_CONTENT)


## Tweets


@app.get('/tweets/',
         response_model=List[Tweet],
         status_code=status.HTTP_200_OK,
         summary='Get all tweets',
         tags=['Tweets'])
def list_tweets() -> List[Tweet]:
    """List tweets.

    This operation path shows all tweets in the app.

    Returns a json with the basic tweet information:
    - **id: UUID**
    - **content: str**
    - **created_by: User**
    - **created_at: datetime**
    - **updated_at: Optional[datetime]**
    """

    if os.path.exists(TWEETS_STORAGE):
        with open(TWEETS_STORAGE, 'r', encoding='utf-8') as f:
            tweets = json.load(f)

    else:
        tweets = []

    return tweets


@app.get('/tweets/{id}',
         response_model=Tweet,
         status_code=status.HTTP_200_OK,
         summary='Get a tweet',
         tags=['Tweets'])
def retrieve_tweet(
    id: str = Path(...,
                   title='Tweet ID',
                   description='The ID of the tweet to retrieve'),
) -> Tweet:
    """Retreive tweet.

    Parameters:
    - Path parameters:
        -   **id: str**

    Returns a json with the tweet information:
    - **id: UUID**
    - **content: str**
    - **created_by: User**
    - **created_at: datetime**
    - **updated_at: Optional[datetime]**
    """

    if os.path.exists(TWEETS_STORAGE):
        with open(TWEETS_STORAGE, 'r', encoding='utf-8') as f:
            tweets = json.load(f)

        for tweet in tweets:
            if tweet['id'] == id:
                return tweet

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Tweet not found')


@app.post('/tweets/',
          response_model=Tweet,
          status_code=status.HTTP_200_OK,
          summary='Create a new tweet',
          tags=['Tweets'])
def create_tweet(tweet: RegisterTweet = Body(...)) -> Tweet:
    """Creates a tweet.

    This path operation creates a new tweet in the app.

    Parameters:
    - Request body parameters:
        - **tweet: RegisterTweet**

    Returns a json with the basic tweet information:
    - **id: UUID**
    - **content: str**
    - **created_at: datetime**
    - **updated_at: Optional[datetime]**
    - **created_by: User**
    """

    # Check if the user exists
    user = None

    if os.path.exists(USERS_STORAGE):
        with open(USERS_STORAGE, 'r', encoding='utf-8') as f:
            raw_users = json.load(f)

        raw_user: dict
        for raw_user in raw_users:
            if raw_user['id'] == tweet.created_by:
                user = raw_user
                break

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    # Save the tweet
    with open(TWEETS_STORAGE, 'w+', encoding='utf-8') as f:
        if os.path.exists(TWEETS_STORAGE):
            try:
                tweets = json.load(f)
                f.seek(0)
                f.truncate()
            except json.JSONDecodeError:
                tweets = []
        else:
            tweets = []

        tweet_dict = {
            'id': str(uuid4()),
            'content': tweet.content,
            'created_at': str(datetime.now()),
            'updated_at': None,
            'created_by': user,
        }

        tweets.append(tweet_dict)
        f.write(json.dumps(tweets))

    return tweet_dict


@app.put('/tweets/{id}',
         response_model=Tweet,
         status_code=status.HTTP_200_OK,
         summary='Update tweet',
         tags=['Tweets'])
def update_tweet(
    id: str = Path(...,
                   title='Tweet ID',
                   description='The ID of the tweet to update'),
    tweet: BaseTweet = Body(...),
) -> Tweet:
    """Update tweet.

    This path operation allows to update the content of a tweet.

    Parameters:
    - Request body parameters:
        - **tweet: BaseTweet**

    Returns a json with the updated tweet information:
    - **id: UUID**
    - **content: str**
    - **created_at: datetime**
    - **updated_at: Optional[datetime]**
    - **created_by: User**
    """

    # Get the tweet
    index = None

    if os.path.exists(TWEETS_STORAGE):
        with open(TWEETS_STORAGE, 'r+', encoding='utf-8') as f:
            tweets = json.load(f)


            for idx, tweet_dict in enumerate(tweets):
                if tweet_dict['id'] == id:
                    index = idx
                    break

            if index is not None:
                tweets[index].update({
                    **tweet.dict(),
                    'updated_at': str(datetime.now()),
                })

                f.seek(0)
                f.truncate()
                f.write(json.dumps(tweets))

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tweet not found',
        )

    return tweets[index]


@app.delete('/tweets/{id}',
            status_code=status.HTTP_204_NO_CONTENT,
            summary='Delete tweet',
            tags=['Tweets'])
def delete_tweet(
    id: str = Path(...,
                   title='Tweet ID',
                   description='The ID of the tweet to delete'),
):
    """Delete tweet.

    This path operation deletes a tweet in the app.

    Parameters:
    - Request body parameters:
        - **tweet: RegisterTweet**
    """

    found = False

    if os.path.exists(TWEETS_STORAGE):
        with open(TWEETS_STORAGE, 'r+', encoding='utf-8') as f:
            raw_tweets = json.load(f)

            tweets = []
            for tweet in raw_tweets:
                if tweet['id'] == id:
                    found = True

                else:
                    tweets.append(tweet)

            if found:
                f.seek(0)
                f.truncate()
                f.write(json.dumps(tweets))

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Tweet not found')

    return Response(status_code=status.HTTP_204_NO_CONTENT)
