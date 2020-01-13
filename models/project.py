import datetime
import uuid
from typing import Dict

import pymongo

from common.Database import Database
from models.shift import Shift


class Project:
    collection = "projects"

    def __init__(self, name: str, time: datetime, weight: float, shift_id: str, path: str, _id: str = None):
        self.name = name
        self.time = time
        self.weight = weight
        self.shift_id = shift_id
        self.shift = Shift.get_by_id(self.shift_id)
        self.path = path
        self.collection = "projects"
        self._id = _id or uuid.uuid4().hex

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "time": self.time,
            "weight": self.weight,
            "shift_id": self.shift_id,
            "path": self.path
        }

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def find_one_by(cls, attribute, value):
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls, attribute, value):
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]

    @classmethod
    def get_by_id(cls, _id):
        return cls.find_one_by("_id", _id)

    @classmethod
    def all(cls):
        return [cls(**project) for project in Database.find("projects", {})]

    @classmethod
    def get_by_search(cls, parameter):
        results = Database.DATABASE[cls.collection].find(
            {"$or":
                [
                    {"name": {"$regex": parameter, "$options": 'i'}},
                    {"path": {"$regex": parameter, "$options": 'i'}}
                ]
             })
        return [cls(**elem) for elem in results]
