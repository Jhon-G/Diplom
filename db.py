from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os


class concert_db():
    '''Create database on pc or server

    '''
    basedir = os.path.abspath(os.path.dirname(__file__))

    engine = create_engine('sqlite:///' + os.path.join(basedir, 'Users_and_Events.db'))

    db_session = scoped_session(sessionmaker(bind=engine))


class Base(concert_db):
    Base = declarative_base()
    Base.query = concert_db.db_session.query_property()
