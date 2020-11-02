import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import MetaData
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

    return session.query(ShopeeItem).filter(ShopeeItem.search_phrase == search_phrase).all()


def GetAllSearchPhrases(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    return [r for (r,) in session.query(ShopeeItem.search_phrase).distinct() \
      .order_by(desc(ShopeeItem.search_phrase))]


def CountShopeeItemWithSearchPhrase(engine, search_phrase):
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(ShopeeItem).filter(ShopeeItem.search_phrase == search_phrase).count()


def CountExistingShopeeItem(engine, shopee_item):
    Session = sessionmaker(bind=engine)
    session = Session()
    count = session.query(ShopeeItem.name, ShopeeItem.seller). \
      filter(ShopeeItem.name == shopee_item.name). \
      filter(ShopeeItem.seller == shopee_item.seller). \
      count()

    return count
