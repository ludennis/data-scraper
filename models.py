import datetime
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ShopeeItem(Base):
    __tablename__ = 'shopee_items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    search_phrase = Column(String)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String)

