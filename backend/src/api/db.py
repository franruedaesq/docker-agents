import os
import sqlmodel
from sqlmodel import Session, SQLModel

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL == "" or DATABASE_URL is None:
    raise NotImplementedError('DATABASE_URL not set')

engine = sqlmodel.create_engine(DATABASE_URL)

# database models
# does not create db migrations
def init_db():
    print('Creating database tables...')
    SQLModel.metadata.create_all(engine)

# apir routes
def get_session():
    with Session(engine) as session:
        yield session