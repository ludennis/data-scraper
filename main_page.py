from flask import Flask
from flask import render_template

from psql_utils import ConnectDatabase
from psql_utils import SelectAllShopeeItems

app = Flask(__name__)
engine = ConnectDatabase(user='d400')


@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/all_shopee_items')
def all_shopee_items():
    items = SelectAllShopeeItems(engine)
    return render_template("show_all_shopee_items.html", items=items)


if __name__ == '__main__':
    app.run(debug=True)
