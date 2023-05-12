import sqlite3
import os
import pytest
import requests
from flask import *
from detective import setup_app
from unittest.mock import patch
from tests import get_imagga_tag_response, get_imagga_upload_response

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
    c.execute("CREATE TABLE IF NOT EXISTS IMAGEOBJECTS(id TEXT, image_id TEXT, object_name TEXT)")
    db.commit()
    db.close()

def teardown_module(module):
    """
    Remove the test SQLite database.
    """
    import os
    os.unlink(IMAGES_DB)


# test uploading image from URL
def test_upload_image(client, mocker):
    """
    Test the POST /images endpoint.
    """
    # Test uploading an image file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'acutedog.jpeg')
    file_data = open(image_path, 'rb').read()

    # mock call to imagga
    mocked_img_response_object = requests.models.Response()
    mocked_img_response_object.status_code = 200
    mocked_img_response_object.json = lambda: get_imagga_upload_response()
    mocker.patch.object(requests, "post", return_value=mocked_img_response_object)
    requests.get("https://api.imagga.com/v2/uploads", data={"image_base64": file_data})

    mocked_tag_response_object = requests.models.Response()
    mocked_tag_response_object.status_code = 200
    mocked_tag_response_object.json = lambda: get_imagga_tag_response()
    mocker.patch.object(requests, "get", return_value=mocked_tag_response_object)
    requests.get("https://api.imagga.com/v2/tags", data={"upload_id": "i05e132196706b94b1d85efb5f3SaM1j"})

    response = client.post('/images', data={"label": "funpic", "image": image_path, "enable_detection": True, "image_type": "file"})

    assert response.status_code == 200
    data = response.json
    assert data["image"]["label"] == "funpic"

    # test uploading image from URL
    url = "http://google.com/very_real_image.png"

    mocked_url_response_object = requests.models.Response()
    mocked_url_response_object.status_code = 200
    mocked_url_response_object._content = file_data
    mocker.patch.object(requests, "get", return_value=mocked_url_response_object)
    requests.get(url)

    mocked_tag_response_object = requests.models.Response()
    mocked_tag_response_object.status_code = 200
    mocked_tag_response_object.json = lambda: get_imagga_tag_response()
    mocker.patch.object(requests, "get", return_value=mocked_tag_response_object)
    requests.get("https://api.imagga.com/v2/tags", data={"image_url": "http://google.com/very_real_image.png"})

    response = client.post('/images', data={"label": "superreal", "image": file_data, "enable_detection": True, "image_type": "url"})
    assert response.status_code == 200
    assert response.json["image"]["label"] == "superreal"


def test_bad_upload_image(client, mocker):
    """
    Test the POST /images endpoint.
    """
    # Test uploading a nonexistent local image file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'NOTAPIC.jpeg')

    response = client.post('/images', data={"label": "funpic", "image": image_path, "enable_detection": True, "image_type": "file"})

    assert response.status_code == 400

    # Test uploading with an image URL that doesn't exist
    url = "http://google.com/very_real_image.png"
    mocked_url_response_object = requests.models.Response()
    mocked_url_response_object.status_code = 404
    mocker.patch.object(requests, "get", return_value=mocked_url_response_object)
    requests.get(url)

    response = client.post('/images', data={"label": "thispicexists", "image": image_path, "enable_detection": True, "image_type": "url"})

    assert response.status_code == 422
    assert response.json["error"] == "There was an issue connecting to Imagga: 404 Client Error: None for url: None"

    # Test uploading with an image URL that is bad
    url = "http://google.com/very_real_image.png"
    mocked_url_response_object = requests.models.Response()
    mocked_url_response_object.status_code = 500
    mocker.patch.object(requests, "get", return_value=mocked_url_response_object)
    requests.get(url)

    response = client.post('/images', data={"label": "thispicexists", "image": image_path, "enable_detection": True, "image_type": "url"})

    assert response.status_code == 422
    assert response.json["error"] == "There was an issue connecting to Imagga: 500 Server Error: None for url: None"
