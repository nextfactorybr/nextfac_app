import uuid
from typing import Dict

from octorest import OctoRest
from common.Database import Database
import json
import datetime


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

    def con(self):
        try:
            con = OctoRest(url=self.url, apikey=self.apikey)
            return con
        except Exception as e:
            return False

    def state(self):
        if self.con() is not False:
            try:
                state = self.con().connection_info()['current']['state']
                error204 = "204 No Content"
                error400 = "400 Bad Request"
                if state != "Closed" and error204 not in state and error400 not in state:
                    return True
            except Exception as e:
                return False
        else:
            return False

    def get_parameters(self):
        if self.state():
            parameters = self.con().printer()
            return parameters
        else:
            return False

    def get_job_info(self):
        if self.state():
            job_info = self.con().job_info()
            return job_info
        else:
            return False

    def get_flag_cancelling(self):
        if self.get_parameters():
            if 'cancelling' in self.get_parameters()['state']['flags']:
                return self.get_parameters()['state']['flags']['cancelling']
        return False

    def get_flag_operational(self):
        if self.get_parameters():
            if 'operational' in self.get_parameters()['state']['flags']:
                return self.get_parameters()['state']['flags']['operational']
        return False

    def get_flag_paused(self):
        if self.get_parameters():
            if 'paused' in self.get_parameters()['state']['flags']:
                return self.get_parameters()['state']['flags']['paused']
        return False

    def get_flag_pausing(self):
        if self.get_parameters():
            if 'pausing' in self.get_parameters()['state']['flags']:
                return self.get_parameters()['state']['flags']['pausing']
        return False

    def get_flag_printing(self):
        if self.get_parameters():
            if 'printing' in self.get_parameters()['state']['flags']:
                return self.get_parameters()['state']['flags']['printing']
        return False

    def get_flag_ready(self):
        if self.get_parameters():
            if 'ready' in self.get_parameters()['state']['flags']:
                return self.get_parameters()['state']['flags']['ready']
        return False

    def get_history(self):
        history = {
            "state": "inactive",
            "cor": "danger",
            "temperature": {
                "tool": 0,
                "bed": 0
            },
            "target": {
                "tool": 0,
                "bed": 0
            },
            "job": {
                "file_name": None,
                "estimatedPrintTime": 0,
                "lastPrintTime": 0,
                "filament_length": 0,
                "completion": 0,
                "printTime": 0,
                "PrintTimeLeft": 0
            }
        }

        if self.state():
            flags = self.get_parameters()['state']['flags'] if 'state' in self.get_parameters() else False
            for flag in flags:
                if flags[flag]:
                    history['state'] = flag

            if history['state'] == "operational" or history['state'] == "ready":
                history['cor'] = "success"
            if history['state'] == "printing":
                history['cor'] = "primary"
            if history['state'] == "pausing" or history['state'] == "paused" or history['state'] == "cancelling":
                history['cor'] = "warning"

            temps = self.get_parameters()['temperature'] if 'temperature' in self.get_parameters() else False
            if temps is not False:
                history['temperature']['tool'] = self.get_tool_temperature(temps) if self.get_tool_temperature(
                    temps) else 0
                history['temperature']['bed'] = self.get_bed_temperature(temps) if self.get_bed_temperature(
                    temps) else 0
                history['target']['tool'] = self.get_tool_target(temps) if self.get_tool_target(temps) else 0
                history['target']['bed'] = self.get_bed_target(temps) if self.get_bed_target(temps) else 0

            job = self.get_job_info()['job'] if 'job' in self.get_job_info() else False
            if job is not False:
                history['job']['estimatedPrintTime'] = job['estimatedPrintTime'] if 'estimatedPrintTime' in job else 0
                # history['job']['estimatedPrintTime'] = str(datetime.timedelta(seconds=job['estimatedPrintTime'])) if 'estimatedPrintTime' in job else 0
                # history['job']['filament_length'] = 0

            file = self.get_job_info()['file'] if 'file' in self.get_job_info() else False
            if file is not False:
                history['job']['file_name'] = file['file_name'] if 'file_name' in file else 0

            progress = self.get_job_info()['progress'] if 'progress' in self.get_job_info() else False
            if progress is not False:
                history['job']['completion'] = progress['completion'] if 'completion' in progress else 0
                history['job']['printTime'] = progress['printTime'] if 'printTime' in progress else 0
                history['job']['PrintTimeLeft'] = progress['PrintTimeLeft'] if 'PrintTimeLeft' in progress else 0

            last_job = self.get_job_info()['lastPrintTime'] if 'lastPrintTime' in self.get_job_info() else False
            if last_job is not False:
                history['job']['lastPrintTime'] = last_job

        return history

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

    @staticmethod
    def connect(printer_id):
        printer = Printer.find_one_by("_id", printer_id)
        con = printer.con()
        if not printer.state():
            try:
                con.connect()
                return True
            except Exception as e:
                raise TypeError(e)

    @staticmethod
    def heat(printer_id):
        printer = Printer.find_one_by("_id", printer_id)
        con = printer.con()
        if printer.state():
            try:
                con.tool_target(215)
                return True
            except Exception:
                return False

    @staticmethod
    def get_bed_temperature(temps):
        if 'bed' in temps:
            return temps['bed']['actual']
        return False

    @staticmethod
    def get_bed_target(temps):
        if 'bed' in temps:
            return temps['bed']['target']
        return False

    @staticmethod
    def get_tool_temperature(temps):
        if 'tool0' in temps:
            return temps['tool0']['actual']
        return False

    @staticmethod
    def get_tool_target(temps):
        if 'tool0' in temps:
            return temps['tool0']['target']
        return False
