from flask import Flask
from flask import render_template

from psql_utils import ConnectDatabase
from psql_utils import GetAllSearchPhrases
from psql_utils import SelectAllShopeeItems
from psql_utils import SelectShopeeItems

from base64 import b64encode

app = Flask(__name__)
engine = ConnectDatabase(user='d400')

@app.route('/')
def index():
    search_phrases = GetAllSearchPhrases(engine)
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

@app.route('/shopee_items_<search_phrase>')
def shopee_items(search_phrase):
    items = SelectShopeeItems(engine, search_phrase)
    for item in items:
        item.image = b64encode(item.image).decode('utf-8')

    return render_template("show_all_shopee_items.html", items=items)


if __name__ == '__main__':
    app.run(debug=True)
