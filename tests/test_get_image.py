import sqlite3
import pytest
from flask import *
from detective import setup_app

# Define test database name
IMAGES_DB = 'user_images.db'

@pytest.fixture
def client():
    """
    Create and return a test client for the Flask application.
    """
    app = Flask(__name__)
    setup_app(app, {})
    with app.test_client() as client:
        yield client

def setup_module(module):
    """
    Set up a test SQLite database with test data.
    """
    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS IMAGES(id TEXT PRIMARY KEY, image BLOB, label TEXT, enable_detection BOOL)")
    c.execute("INSERT OR IGNORE INTO IMAGES (id, image, label, enable_detection) VALUES (1, 1001, 'cutepuppies', True)")
    c.execute("INSERT OR IGNORE INTO IMAGES (id, image, enable_detection) VALUES (2, NULL, False)")
    c.execute("INSERT OR IGNORE INTO IMAGES (id, image, label, enable_detection) VALUES (3, 0110, 'smallkittens', True)")
    c.execute("CREATE TABLE IF NOT EXISTS IMAGEOBJECTS(id TEXT, object_name TEXT, image_id TEXT)")
    c.execute("INSERT OR IGNORE INTO IMAGEOBJECTS (id, object_name, image_id) VALUES (5678, 'dog', 1)")
    db.commit()
    db.close()

def teardown_module(module):
    """
    Remove the test SQLite database.
    """
    import os
    os.unlink(IMAGES_DB)

def test_get_image(client):
    """
    Test the GET /images/<image_id> endpoint.
    """
    # Test a valid ID
    response = client.get('/images/1')
    assert response.status_code == 200
    data = response.json["image"]
    assert data["label"] == "cutepuppies"
    assert data['objects'][0] == 'dog'

    # Test an invalid ID
    response = client.get('/images/9348594328')
    assert response.status_code == 404
    assert response.json == {'error': 'Image not found'}

def test_get_all_images(client):
    """
    Test the GET /images endpoint without query.
    """
    response = client.get('/images')
    assert response.status_code == 200
    data = response.json["images"][0]
    assert data["label"] == "cutepuppies"
    assert data['objects'][0] == 'dog'

    data = response.json["images"][2]
    assert data["label"] == "smallkittens"
    assert data['objects'] == None

def test_get_image_by_object(client):
    """
    Test the GET /images endpoint with query.
    """
    # Test a valid query
    response = client.get('/images?objects=dog')
    assert response.status_code == 200
    data = response.json["images"][0]
    print(data, "^^^^^^^^^^^^^^^")
    assert data["label"] == "cutepuppies"
    assert data['objects'][0] == 'dog'

    # Test an object that hasn't been detected
    response = client.get('/images?objects=pickles')
    assert response.status_code == 404
    assert response.json == {'error': 'Image not found'}
