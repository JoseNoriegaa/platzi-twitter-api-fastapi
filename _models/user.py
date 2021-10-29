from typing import Optional
from datetime import date

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# Mixins
from mixins.models import IDMixin
from mixins.models import TimestampMixin


class BaseUser(BaseModel):
    email: Optional[EmailStr] = Field(...,
                                      description='User\'s email',
                                      example='johndoe@example.com')


class UserProfile(BaseModel):
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


class User(IDMixin, UserProfile, TimestampMixin, BaseUser):
    pass


class PasswordMixin(BaseModel):
    password: str = Field(...,
                          min_length=8,
                          max_length=64,
                          example='password',)


class UserLogin(PasswordMixin, BaseUser):
    pass


class UserRegister(PasswordMixin, UserProfile, BaseUser):
    pass
