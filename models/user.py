import datetime


from datetime import date, datetime

# SSQLAlchemy
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import Date
from sqlalchemy import text
from sqlalchemy.sql import func


# Database
from config.db import meta


User = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String(50), nullable=False),
    Column('last_name', String(50), nullable=False),
    Column('birth_date', Date, nullable=True),
    Column('email', String(120), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow),
)
