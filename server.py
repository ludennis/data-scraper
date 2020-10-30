from flask import Flask
from flask import render_template

from psql_utils import ConnectDatabase
from psql_utils import SelectAllShopeeItems

from base64 import b64encode

app = Flask(__name__)
engine = ConnectDatabase(user='d400')


@app.route('/')
def index():
    return render_template("index.html")

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
