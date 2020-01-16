import uuid
from typing import Dict

from common.Database import Database


class Filament:
    collection = "filaments"

    def __init__(self, cor: str, temp: int, filament_type: str, provider: str, cost: float, quality: int, stock: int,
                 weight: str, name: str, _id: str = None):
        self.cor = cor
        self.temp = temp
        self.filament_type = filament_type
        self.provider = provider
        self.cost = cost
        self.quality = quality
        self.stock = stock
        self.weight = weight
        self.name = name
        self.collection = "filaments"
        self._id = _id or uuid.uuid4().hex

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "cor": self.cor,
            "temp": self.temp,
            "filament_type": self.filament_type,
            "provider": self.provider,
            "cost": self.cost,
            "quality": self.quality,
            "stock": self.stock,
            "weight": self.weight,
            "name": self.name
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
    def all(cls,  skip=0, limit=0):
        return [cls(**filament) for filament in Database.find("filaments", {}).skip(skip).limit(limit)]

    @classmethod
    def get_by_search(cls, parameter):
        results = Database.DATABASE[cls.collection].find(
            {"$or":
                [
                    {"provider": {"$regex": parameter, "$options": 'i'}},
                    {"cor": {"$regex": parameter, "$options": 'i'}}
                ]
            })
        return [cls(**elem) for elem in results]
