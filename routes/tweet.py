from typing import List
from datetime import datetime

# PyDottie
import pydottie  # type: ignore

# SQLAlchemy
from sqlalchemy import text


# FastAPI
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi import Body
from fastapi import Path
from fastapi import Depends

# Models
from models import Tweet

# Database
from config.db import connection

# Schemas
from schemas.tweet import Tweet as TweetOut
from schemas.tweet import TweetWithRelations
from schemas.tweet import BaseTweet
from schemas.user import User as UserSchema

# Middlewares
from middleware.auth import get_current_user

router = APIRouter()


@router.get('/',
            response_model=List[TweetWithRelations],
            status_code=status.HTTP_200_OK,
            summary='Get all tweets',
            tags=['Tweets'])
def list_tweets():
    """List tweets.

    This operation path shows all tweets in the app.

    Returns a json with the basic tweet information:
    - id: **int**
    - content: **str**
    - user: **UserOut**
    - created_at: **datetime**
    - updated_at: **datetime**
    """

    # TODO: Change the raw query to a SQLAlchemy query
    query = """
    SELECT
        t.id as 'id',
        t.content as 'content',
        t.created_at as 'created_at',
        t.updated_at as 'updated_at',
        u.id as 'user.id',
        u.first_name as 'user.first_name',
        u.last_name as 'user.last_name',
        u.birth_date as 'user.birth_date',
        u.email as 'user.email',
        u.created_at as 'user.created_at',
        u.updated_at as 'user.updated_at'
    FROM
        tweets as t
    INNER JOIN
        users as u
    ON
        t.user_id = u.id;
    """

    response = connection.execute(text(query)).fetchall()

    output = []
    for record in response:
        output.append(pydottie.transform(record))

    return output


@router.get('/{id}',
            response_model=TweetWithRelations,
            status_code=status.HTTP_200_OK,
            summary='Get a tweet',
            tags=['Tweets'])
def retrieve_tweet(
    id: int = Path(...,
                   title='Tweet ID',
                   description='The ID of the tweet to retrieve'),
):
    """Retreive tweet.

    Parameters:
    - Path parameters:
        - id: **str**

    Returns a json with the tweet information:
    - id: **int**
    - content: **str**
    - user: **UserOut**
    - created_at: **datetime**
    - updated_at: **datetime**
    """

    query = """
    SELECT
        t.id as 'id',
        t.content as 'content',
        t.created_at as 'created_at',
        t.updated_at as 'updated_at',
        u.id as 'user.id',
        u.first_name as 'user.first_name',
        u.last_name as 'user.last_name',
        u.birth_date as 'user.birth_date',
        u.email as 'user.email',
        u.created_at as 'user.created_at',
        u.updated_at as 'user.updated_at'
    FROM
        tweets as t
    INNER JOIN
        users as u
    ON
        t.user_id = u.id
    WHERE
        t.id = :id
    ;
    """

    tweet = connection.execute(text(query), id=id).fetchone()

    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Tweet not found')

    return pydottie.transform(tweet)


@router.post('/',
          response_model=TweetOut,
          status_code=status.HTTP_200_OK,
          summary='Create a new tweet',
          tags=['Tweets'])
def create_tweet(
    tweet: BaseTweet = Body(...),
    request_user: UserSchema = Depends(get_current_user),
):
    """Creates a tweet.

    This path operation creates a new tweet in the app.

    Parameters:
    - Request body parameters:
        - tweet: **BaseTweet**

    Returns a json with the basic tweet information:
    - id: **int**
    - content: **str**
    - created_at: **datetime**
    - updated_at: **datetime**
    - user_id: **int**
    """

    # Create tweet
    tweet_dict = tweet.dict()
    tweet_dict['user_id'] = request_user.id

    response = connection.execute(Tweet.insert().values(**tweet_dict))

    if response is None or (response.rowcount == 0):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Something went wrong.')

    tweet_dict['id'] = response.lastrowid
    tweet_dict['created_at'] = datetime.utcnow()
    tweet_dict['updated_at'] = tweet_dict['created_at']

    return tweet_dict


@router.put('/{id}',
         response_model=TweetWithRelations,
         status_code=status.HTTP_200_OK,
         summary='Update tweet',
         tags=['Tweets'])
def update_tweet(
    id: str = Path(...,
                   title='Tweet ID',
                   description='The ID of the tweet to update'),
    tweet: BaseTweet = Body(...),
    request_user: UserSchema = Depends(get_current_user),
):
    """Update tweet.

    This path operation allows to update the content of a tweet.

    Only the tweet owner can update the tweet.

    Parameters:
    - Request body parameters:
        - tweet: **BaseTweet**

    Returns a json with the updated tweet information:
    - id: **int**
    - content: **str**
    - created_at: **datetime**
    - updated_at: **Optional[datetime]**
    - user: **UserOut**
    """

    tweet_response = connection.execute(Tweet.select().where(Tweet.c.id == id)).fetchone()

    if tweet_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Tweet not found')

    if tweet_response.user_id != request_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to update this tweet')

    connection.execute(Tweet.update().where(Tweet.c.id == id).values(**tweet.dict()))

    tweet_dict = {**tweet_response}
    tweet_dict['updated_at'] = datetime.utcnow()
    tweet_dict['user'] = request_user

    return tweet_dict


@router.delete('/{id}',
            status_code=status.HTTP_204_NO_CONTENT,
            summary='Delete tweet',
            tags=['Tweets'])
def delete_tweet(
    id: int = Path(...,
                   gt=0,
                   title='Tweet ID',
                   description='The ID of the tweet to delete'),
    request_user: UserSchema = Depends(get_current_user),
):
    """Delete tweet.

    This path operation deletes a tweet in the app.

    Only the tweet owner can delete the tweet.

    Parameters:
    - Request body parameters:
        - tweet: **BaseTweet**
    """

    tweet_response = connection.execute(Tweet.select().where(Tweet.c.id == id)).fetchone()

    if tweet_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Tweet not found')

    if tweet_response.user_id != request_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to delete this tweet')

    connection.execute(Tweet.delete().where(Tweet.c.id == id))

    return Response(status_code=status.HTTP_204_NO_CONTENT)
