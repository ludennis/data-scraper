from flask import Flask
from flask import render_template

from psql_utils import ConnectDatabase
from psql_utils import SelectAllShopeeItems

from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker

from models import ShopeeItem

from base64 import b64encode

app = Flask(__name__)
engine = ConnectDatabase(user='d400')


@app.route('/')
def index():
    Session = sessionmaker(bind=engine)
    session = Session()
    table = ShopeeItem.__table__.name
    search_phrases = [r for (r,) in session.query(ShopeeItem.search_phrase).distinct()]
    for search_phrase in search_phrases:
        print("search_phrase: {}".format(search_phrase))
        print("Type of search_phrase: {}".format(type(search_phrase)))
    return render_template("index.html", search_phrases=search_phrases)

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/all_shopee_items')
def all_shopee_items():
    items = SelectAllShopeeItems(engine)
    for item in items:
        item.image = b64encode(item.image).decode('utf-8')
    return render_template("show_all_shopee_items.html", items=items)


if __name__ == '__main__':
    app.run(debug=True)
