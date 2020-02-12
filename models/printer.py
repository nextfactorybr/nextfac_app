import uuid
from typing import Dict

from octorest import OctoRest
from common.Database import Database


class Printer:
    collection = "printers"

    def __init__(self, name: str, url: str, apikey: str, server: bool = None, _id: str = None):
        self.server = server
        self.name = name
        self.url = url
        self.apikey = apikey
        self.collection = "printers"
        self._id = _id or uuid.uuid4().hex

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "apikey": self.apikey,
            "server": self.server
        }

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def find_one_by(cls, attribute, value):
        result = Database.find_one(cls.collection, {attribute: value})
        return cls(**result) if result else None

    @classmethod
    def find_many_by(cls, attribute, value):
        result = Database.find(cls.collection, {attribute: value})
        return [cls(**elem) for elem in result] if result else None

    @classmethod
    def get_by_id(cls, _id):
        return cls.find_one_by("_id", _id)

    @classmethod
    def all(cls, skip=0, limit=0):
        result = Database.find("printers", {}).sort("name").skip(skip).limit(limit)
        return [cls(**printer) for printer in result] if result else None

    @staticmethod
    def connect(printer_id):
        printer = Printer.find_one_by("_id", printer_id)
        con = OctoRest(url=printer.url, apikey=printer.apikey)
        error_str = "Failed to autodetect serial port"
        if con.state() == 'Closed' or error_str in con.state():
            try:
                con.connect()
                return True
            except Exception as e:
                raise TypeError(e)

    @staticmethod
    def heat(printer_id):
        printer = Printer.find_one_by("_id", printer_id)
        con = OctoRest(url=printer.url, apikey=printer.apikey)
        if con.state() == 'Operational':
            try:
                con.tool_target(215)
                return True
            except Exception as e:
                raise TypeError(e)

    @classmethod
    def get_by_search(cls, parameter):
        result = Database.DATABASE[cls.collection].find(
            {"$or":
                [
                    {"name": {"$regex": parameter, "$options": 'i'}},
                    {"url": {"$regex": parameter, "$options": 'i'}}
                ]
            })
        return [cls(**elem) for elem in result] if result else None
