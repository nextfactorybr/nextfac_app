import uuid
from typing import Dict

from octorest import OctoRest
from common.Database import Database


class Printer:
    collection = "printers"

    def __init__(self, name: str, url: str, apikey: str, _id: str = None):
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
            "apikey": self.apikey
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
        return [cls(**printer) for printer in Database.find("printers", {})]

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
