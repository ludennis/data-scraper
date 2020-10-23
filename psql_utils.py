import datetime
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from getpass import getpass

Base = declarative_base()


class ShopeeItem(Base):
    __tablename__ = 'shopee_items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    search_phrase = Column(String)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String)


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
