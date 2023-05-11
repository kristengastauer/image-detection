import uuid
import sqlite3

class ImageObjects:

    def __init__(self, id=None, image_id=None, object_name=None):
        if id is not None:
            self.id = id
        else:
            self.id = uuid.uuid4().hex  # id of the join
        self.image_id = image_id
        self.object_name = object_name

    def add_to_db(self):
        db = sqlite3.connect("user_images.db")
        c = db.cursor()

        c.execute("INSERT INTO IMAGEOBJECTS (id, image_id, object_name) VALUES (?, ?, ?)",
                    (self.id, self.image_id, self.object_name))
        db.commit()
        return self
    
    @classmethod
    def get_all_image_ids_by_object(cls, object_name):
        c = sqlite3.connect("user_images.db").cursor()
        name = object_name.strip('"')
        c.execute("SELECT * FROM IMAGEOBJECTS WHERE object_name=?", (name,))
        data = c.fetchall()
        image_ids = []
        for row in data:
            formatted = cls(*row)
            image_ids.append(formatted.image_id)
        return image_ids