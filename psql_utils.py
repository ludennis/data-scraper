import datetime
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from getpass import getpass

from models import Base
from models import ShopeeItem


def ConnectDatabase(user: str, db_name: str='scraper_db', host: str='localhost'):
    password = getpass(prompt='Password of user: ')

    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format( \
      user, password, host, db_name))

    return engine


def InitializePostgreSQLDatabase(engine):
    Base.metadata.create_all(engine)


def InsertItem(engine, name, price, search_phrase, url):
    item = ShopeeItem(name=name, price=price, search_phrase=search_phrase, url=url)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(item)
    session.commit()
