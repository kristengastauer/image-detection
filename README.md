# image-detection
API that processes provided images for objects and returns the image(s)


# API Specification

## Get all images
```
GET /images
```
Response | Description
---------|------------
200      | Json with all image metadata

Sample response
```
{"images": [{"id": 12345678654323456, "label": "superreal", "enable_detection": 1, "objects": ["dog"]}]}
```

## Get all images containing an object
```
GET /images?objects="dog,cat"
```
Response | Description
---------|------------
200      | Json with images containing query
404      | Images containing objects not found

Parameter | Description
----------|-------------
objects   | comma-separated list of objects to detect

Sample response
```
{"images": [{"id": 12345678654323456, "label": "superreal", "enable_detection": 1, "objects": ["dog"]}]}
```

## Get one image's metadata
```
GET /images/{image_id}
```
Response | Description
---------|------------
200      | Json with all image metadata
404      | Image with ID not found

Parameter | Description
----------|-------------
image_id  | path parameter ID of specified image

Sample response
```
{"image": {"id": 12345678654323456, "label": "superreal", "enable_detection": 1, "objects": ["dog"]}}
```

## Post an image and recieve it's metadata, the objects detected in it
```
POST /images
```
Response | Description
---------|------------
200      | Json with all image data, label, DB ID, any objects detected (if enabled)
400      | Bad image data provided

Parameter            | Description
---------------------|-------------
image                | image file (in binary format) or URL
label                | (optional) label for image (default is auto-generated value)
enable_detection     | (optional) enable image detection for provided image (defaulted false)
image_type           | (optional - defaults type is "file") should be either "file" or "url" to process image type

Sample response
```
{"image": {"id": 12345678654323456, "label": "superreal", "enable_detection": 1, "objects": ["dog"]}}
{"image": {"id": 12345678654323456, "label": "superreal", "enable_detection": 0, "objects": None}}
```

# Image object detection: Imagga

https://docs.imagga.com/#tags
https://docs.imagga.com/#uploads



# Local Setup

```
sudo pip3 install virtualenv
python3 -m virtualenv image-detection
cd image-detection
source bin/activate
pip install -r requirements.txt
python3 dev.py
```

To run the UI (since these are on the same port, you must run UI before dev.py):
```
cd app
npm start
```

To test the API directly, in a second terminal window you can now hit:
```
curl -X GET http://localhost:8080/images

curl -X POST http://localhost:8080/images -F "image=<url>" -F "image_type=url" -F "label=fluffy_dog" -F "enable_detection=False"
```


# Future Iterations and development

### Extra API Endpoints For UI
```
GET /images/objects
```
Response | Description
---------|------------
200      | List of all objects in images db

If we had this endpoint, we could show options for the UI to show the user to filter on

### API Security

- Ensure users are authorized to use the API
- Ensure that users are accessing their own images uploaded, and not others

### Query specifications

- Allow for semi-match cases for object searches
Example:
```
GET /images?objects="dog,cat"

{"images": [
        {"id": 12345678654323456, "label": "cockapooAndyorkie", "enable_detection": 1, "objects": ["fluffy dog", "dogs"]},
        {"id": 12345678654323456, "label": "lion", "enable_detection": 1, "objects": ["jungle cat"]}
    ]
}
```