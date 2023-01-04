from flask import Flask
from flask import render_template

from base64 import b64encode

app = Flask(__name__)

@app.route('/')
def hello():
    return '<p>Hello, World!</p>'

if __name__ == '__main__':
    app.run(debug=True)
