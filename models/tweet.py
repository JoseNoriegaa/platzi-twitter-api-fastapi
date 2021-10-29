from datetime import datetime

# SQLAlchemy
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey

# Database
from config.db import meta


# Tweet table
Tweet = Table(
    'tweets',
    meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('content', String(255), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False,),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow),
)
