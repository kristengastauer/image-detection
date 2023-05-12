from flask import *
from detective import setup_app

CONFIG = {}

def run():
    app = Flask(__name__)
    setup_app(app, CONFIG)
    app.run(debug=True, port=3000)

if __name__ == "__main__":
    run()