# SQLAlchemy
from sqlalchemy import create_engine   # type: ignore
from sqlalchemy import MetaData  # type: ignore

# Local
from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

meta = MetaData()

connection = engine.connect()
