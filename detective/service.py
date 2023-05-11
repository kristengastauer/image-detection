import sqlite3
import json
import requests
from flask import jsonify
from detective.model import UserImage, ImageObjects
from detective.lib import imagga

def get_all_images():
    images = UserImage.get_all()
    return images

def get_image_by_id(id):
    return UserImage.get_by_id(id)

def add_image(label, image, enable_detection, typ="file"):
    # convert image to binary
    # call to see objects detected
    objects = []
    if typ == "url":
        binary_img = _convert_url_to_binary(image)
        if enable_detection:
            objects = imagga.get_tags_for_image_url(img_url=image)
    else:
        if (not isinstance(image, str) or not image.strip()):
            return {'error': 'Invalid image file.'}
        with open(image, 'rb') as file:
            if enable_detection:
                upload_id = imagga.upload_image_for_processing(file)
                objects = imagga.get_tags_for_image_url(upload_id=upload_id)
            binary_img = file.read()

    # add image to db
    img = UserImage(id=None,
                    image=binary_img,
                    label=label,
                    enable_detection=enable_detection
                    )
    img.add_to_db()
    if img.enable_detection:
        # add objs to db
        for obj in objects:
            img_obj = ImageObjects(id=None, image_id=img.id, object_name=obj)
            img_obj.add_to_db()

    return img.to_dict()

def get_all_images_by_object(object_name):
    image_ids = ImageObjects.get_all_image_ids_by_object(object_name)
    if len(image_ids) == 0:
        return
    images = []
    for id in image_ids:
        img_meta = get_image_by_id(id)
        images.append(img_meta)

    return images

def _convert_url_to_binary(file_url):
    r = requests.get(file_url)
    r.raise_for_status()
    return r.content
