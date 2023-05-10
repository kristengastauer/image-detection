import uuid

class ImageObjects:

    def __init__(self, image_id, object_name):
        self.id = uuid.uuid4().hex  # id of the join
        self.object_name = object_name
        self.image_id = image_id
