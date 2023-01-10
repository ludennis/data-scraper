from flask import Flask
from flask import render_template

from base64 import b64encode

app = Flask(__name__)

@app.route('/')
def hello():
    return '<p>Hello World Updated!!!</p>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
