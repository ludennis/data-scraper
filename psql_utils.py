import psycopg2
from sqlalchemy import MetaData
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


def InsertShopeeItem(engine, item: ShopeeItem):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(item)
    session.commit()


def InsertItem( \
  engine, name, price, search_phrase, url, image, seller, brand, quantity, location, description):
    item = ShopeeItem( \
      name, price, search_phrase, url, image, seller, brand, quantity, location, description)
    InsertShopeeItem(engine, item)


def SelectAllShopeeItems(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(ShopeeItem).all()


def SelectShopeeItems(engine, search_phrase):
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(ShopeeItem).filter(ShopeeItem.search_phrase == search_phrase)


def GetAllSearchPhrases(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    return [r for (r,) in session.query(ShopeeItem.search_phrase).distinct()]


def CountExistingShopeeItem(engine, shopee_item):
    Session = sessionmaker(bind=engine)
    session = Session()
    table = ShopeeItem.__table__.name
    count = session.query(ShopeeItem.name, ShopeeItem.seller). \
      filter(ShopeeItem.name == shopee_item.name). \
      filter(ShopeeItem.seller == shopee_item.seller). \
      count()

    return count
