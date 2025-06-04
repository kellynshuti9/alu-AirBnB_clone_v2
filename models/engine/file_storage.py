#!/usr/bin/python3
"""File storage engine"""

import json
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Handles serialization and deserialization of objects to/from JSON"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns all stored objects, optionally filtered by class"""
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            return {
                key: obj for key, obj in self.__objects.items()
                if isinstance(obj, cls)
            }
        return self.__objects

    def new(self, obj):
        """Adds a new object to storage dictionary"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        obj_dict = {
            key: obj.to_dict() for key, obj in self.__objects.items()
        }
        with open(self.__file_path, 'w', encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes JSON file back to __objects"""
        try:
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                obj_data = json.load(f)
                for key, val in obj_data.items():
                    cls = val["__class__"]
                    self.__objects[key] = eval(cls)(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it exists"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """Reloads the storage from the JSON file"""
        self.reload()
