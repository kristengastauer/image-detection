from flask import Blueprint, request, jsonify, abort
import json
import detective.service as image_service


def create(config):
    app = Blueprint('images', __name__)

    @app.route('/images', methods=['GET'])
    def get_images():
        objects = request.args.get("objects")
        # no query of objects, return them all
        if not objects:
            return {"images": json.loads(image_service.get_all_images())}

        # otherwise, call to get all images with object detection enabled that have object
        images = []
        objects = objects if isinstance(objects, list) else [objects]
        for obj in objects:
            matches = image_service.get_all_images_by_object(obj)
            if matches:
                for row in matches:
                    images.append(row)

        if len(images) == 0:
            return _not_found("Image not found")

        return {"images": images}
        

    @app.route('/images/<image_id>', methods=['GET'])
    def get_image(image_id):
        image = image_service.get_image_by_id(image_id)
        if not image:
            return _not_found("Image not found")

        return {"image": image}

    @app.route('/images', methods=['POST'])
    def add_image():
        label = request.form.get("label")
        image = request.form.get("image")
        typ = request.form.get("image_type")
        enable_detection = request.form.get("enable_detection")

        image = image_service.add_image(label, image, enable_detection, typ=typ)
        return {"image": image}

    def _not_found(message):
        response = jsonify({'error': message})
        response.status_code = 404
        return response

    return app
