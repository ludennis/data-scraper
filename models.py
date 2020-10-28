import datetime
from sqlalchemy import Column, Integer, DateTime, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ShopeeItem(Base):
    def __repr__(self):
        return {'item_id': self.item_id, 'name':self.name}


    def __str__(self):
        return '{}: {}'.format(self.item_id, self.name)

    __tablename__ = 'shopee_items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    search_phrase = Column(String)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String)
    image = Column(LargeBinary)
