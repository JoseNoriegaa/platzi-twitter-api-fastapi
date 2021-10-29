# Pydantic
from pydantic import BaseModel
from pydantic import Field

# Models
from schemas.user import UserOut

# Mixins
from mixins.models import IDMixin
from mixins.models import TimestampMixin



class BaseTweet(BaseModel):
    content: str = Field(...,
                        min_length=1,
                        max_length=256,)


class TweetUserID(BaseModel):
    user_id: int = Field(...,
                         ge=1,
                         title='User who created the tweet',
                         example=1,)


class Tweet(TweetUserID, IDMixin, TimestampMixin, BaseTweet):
    pass


class TweetWithRelations(IDMixin, TimestampMixin, BaseTweet):

    user: UserOut = Field(...,
                       title='User who created the tweet',)


class RegisterTweet(TweetUserID, BaseTweet):
    pass
