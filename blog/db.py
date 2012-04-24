from blog import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = None
session = None


def make_session():
    global engine, session
    engine = create_engine(app.config['DATABASE_URL'], convert_unicode=True)
    session = scoped_session(sessionmaker(bind=engine))


def init_db():
    Base.metadata.create_all(engine)


@app.teardown_request
def remove_db_session(exception):
    session.remove()
