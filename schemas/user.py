from datetime import date
from typing import Optional

# Pydantic
from typing import Optional
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# Mixins
from mixins.models import IDMixin
from mixins.models import TimestampMixin


class PasswordMixin(BaseModel):
    password: str = Field(...,
                          min_length=8,
                          max_length=255,
                          example='password',)


class BaseUser(BaseModel):
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

    email: EmailStr = Field(...,)

    birth_date: Optional[date] = Field(default=None,
                                       title='Birth date',
                                       example='2021-01-01',)



class UserOut(IDMixin, TimestampMixin, BaseUser):
    pass


class User(PasswordMixin, UserOut):
    pass


class CreateUser(PasswordMixin, BaseUser):
    pass
