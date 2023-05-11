import random
import string
import uuid
import sqlite3
LABEL_LENGTH = 10
from detective.model import ImageObjects

class UserImage:

    def __init__(self, id=None, image=None, label=None, enable_detection=False):
        self.id = id
        if not id:
            self.id = uuid.uuid4().hex
        if not label:
            label = str(self.id)
        self.label = label  # string
        self.image = image  # blob
        self.enable_detection = bool(enable_detection)  # bool

    def to_dict(self):
        objs = self.get_all_detected_objects()
        return {
            "id": self.id,
            "label": self.label,
            "enable_detection": self.enable_detection,
            "objects": objs
        }
    
    @classmethod
    def get_all(cls):
        c = sqlite3.connect("user_images.db").cursor()
        c.execute("SELECT id, image, label, enable_detection FROM IMAGES")
        images = []
        for row in c.fetchall():
            item = UserImage(*row)
            images.append(item.to_dict())
        c.close()
    
        return images
    
    def get_all_detected_objects(self):
        c = sqlite3.connect("user_images.db").cursor()
        c.execute("SELECT * FROM IMAGEOBJECTS WHERE image_id=?", (self.id,))
        data = c.fetchall()
        
        if len(data) == 0:
            return
        detected_objs = []
        for row in data:
            obj = ImageObjects(*row)
            detected_objs.append(obj.object_name)

        return detected_objs
    
    def add_to_db(self):
        db = sqlite3.connect("user_images.db")
        c = db.cursor()
        c.execute("INSERT INTO IMAGES VALUES(?,?,?,?)",
                (self.id, self.image, self.label, self.enable_detection))
        db.commit()
        return self

    @classmethod
    def get_by_id(cls, id):
        c = sqlite3.connect("user_images.db").cursor()
        c.row_factory = sqlite3.Row
        c.execute("SELECT id, image, label, enable_detection FROM IMAGES WHERE id=?", (id,))
        row = c.fetchone()
        if not row:
            return None
        formatted = cls(*row)
        
        return formatted.to_dict()
