# Pydantic
from pydantic import BaseModel
from pydantic import Field

# Models
from models.user import User

# Mixins
from mixins.models import TimestampMixin
from mixins.models import IDMixin


class BaseTweet(BaseModel):
    content: str = Field(...,
                        min_length=1,
                        max_length=256,)


class Tweet(IDMixin, TimestampMixin, BaseTweet):

    created_by: User = Field(...,
                             title='User who created the tweet',)


class RegisterTweet(BaseTweet):

    created_by: str = Field(...,
                            title='ID of the user who created the tweet',)
