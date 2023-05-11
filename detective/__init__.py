from flask import *
import sqlite3

from detective.api import images

def setup_app(app, config):
    imgs = sqlite3.connect("user_images.db").cursor()
    imgs.execute("CREATE TABLE IF NOT EXISTS IMAGES("
              "id TEXT PRIMARY KEY, image BLOB, label TEXT, enable_detection BOOL)"
              )
    imgs.execute("CREATE TABLE IF NOT EXISTS IMAGEOBJECTS("
              "id TEXT, image_id TEXT, object_name TEXT)"
              )
    imgs.connection.close()
    app.register_blueprint(images.create(config))

def init(config):
    app = Flask(__name__)
    setup_app(app, config)
