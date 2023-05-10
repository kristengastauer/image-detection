import sqlite3
import json
import requests
from io import BytesIO
from PIL import Image
from flask import jsonify
from detective.model import UserImage, ImageObjects
from detective.lib import imagga

def get_all_images():
    c = sqlite3.connect("user_images.db").cursor()
    c.execute("SELECT id, image, label, enable_detection FROM IMAGES")
    images = []
    for row in c.fetchall():
        item = UserImage(*row)
        images.append(item.to_dict())
    c.close()
    return json.dumps(images)

def get_image_by_id(id):
    c = sqlite3.connect("user_images.db").cursor()
    c.row_factory = sqlite3.Row
    rows = c.execute("SELECT id, image, label, enable_detection FROM IMAGES WHERE id=?", (id,))
    formatted = []
    for row in rows:
        item = UserImage(*row)
        formatted.append(item.to_dict())
    if len(formatted) == 0:
        return
    return formatted[0]

def add_image(label, image, enable_detection, typ="file"):
    # convert image to binary
    binary_img = image
    if typ == "url":
        binary_img = _convert_url_to_binary(image)

    # add image to db
    img = _add_image_to_db(label, binary_img, enable_detection)

    # call to see objects detected
    if img["enable_detection"]:
        if typ == "url":
            objects = imagga.get_tags_for_image_url(img_url=image)
        else:
            upload_id = imagga.upload_image_for_processing(binary_img)
            objects = imagga.get_tags_for_image_url(upload_id=upload_id)

        # add objs to db
        for obj in objects:
            _add_object_to_db(img["id"], obj)

    return img

def get_all_images_by_object(object_name):
    c = sqlite3.connect("user_images.db").cursor()
    c.execute("SELECT * FROM IMAGEOBJECTS WHERE object_name=?", (object_name,))
    data = c.fetchall()
    if len(data) == 0:
        return
    images = []
    image_ids = [row[2] for row in data]
    print(image_ids, "%%%%%%%%%%%%%%%%%%%")
    for id in image_ids:
        img_meta = get_image_by_id(id)
        print(img_meta, "@#$%^&@#$%^&*@#$%^&")
        images.append(img_meta)

    return images

def _add_image_to_db(label, image, enable_detection):
    db = sqlite3.connect("user_images.db")
    c = db.cursor()
    img = UserImage(image=image,
                    label=label,
                    enable_detection=enable_detection
                    )

    c.execute("INSERT INTO IMAGES VALUES(?,?,?,?)",
              (img.id, img.label, img.image, img.enable_detection))
    db.commit()
    return img.to_dict()

def _add_object_to_db(image_id, object_name):
    db = sqlite3.connect("user_images.db")
    c = db.cursor()
    img_obj = ImageObjects(image_id, object_name)

    c.execute("INSERT INTO IMAGEOBJECTS (id, image_id, object_name) VALUES (?, ?, ?)",
                (img_obj.id, image_id, object_name))
    db.commit()
    return img_obj

def _convert_url_to_binary(file_url):
    r = requests.get(file_url)
    r.raise_for_status()
    return r.content
