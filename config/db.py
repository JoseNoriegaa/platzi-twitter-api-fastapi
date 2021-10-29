# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import MetaData

# Local
from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

meta = MetaData()

connection = engine.connect()
