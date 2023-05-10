from flask import *
import sys

CONFIG = {}

def run():
    app = Flask(__name__)
    sys.path.append('./detective')
    from detective import setup_app
    from detective.service import open_db
    setup_app(app, CONFIG)
    open_db()
    app.run(debug=True, port=8080)
