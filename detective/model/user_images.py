import random
import string
import uuid
import sqlite3
LABEL_LENGTH = 10

class UserImage:

    def __init__(self, id=None, image=None, label=None, enable_detection=True):
        self.id = id
        if not id:
            self.id = uuid.uuid4().hex
        if not label:
            label = str(self.id)
        self.label = label  # string
        self.image = image  # blob
        self.enable_detection = enable_detection  # bool

    def to_dict(self):
        objs = self.get_all_detected_objects()
        print(objs, "$$$$$$$$$$$$$$$$$$$$$$$$$$")
        return {
            "id": self.id,
            "label": self.label,
            "enable_detection": self.enable_detection,
            "objects": objs
        }
    
    def get_all_detected_objects(self):
        c = sqlite3.connect("user_images.db").cursor()
        print(self.id, "****************************")
        c.execute("SELECT * FROM IMAGEOBJECTS WHERE image_id=?", (self.id,))
        data = c.fetchall()
        
        if len(data) == 0:
            return
        detected_objs = []
        for row in data:
            print(row, '%%%%%%%%%%%%%%%%%%%%%%')
            detected_objs.append(row[1])

        return detected_objs

