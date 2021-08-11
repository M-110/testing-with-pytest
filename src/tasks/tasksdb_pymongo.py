"""Database wrapper for TinyDB"""
import os
import subprocess
import time
from typing import List

import pymongo
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure


class TasksDB_MongoDB:
    """Wrapper class for MongoDB."""

    def __init__(self, db_path: str) -> None:
        """Connect to db."""
        self._process = None
        self._client = None
        self._db = None
        self._start_mongod(db_path)
        self._connect()

    def _start_mongod(self, db_path):
        """Start mongo db process."""
        self._process = subprocess.Popen(['mongod', '--dbpath', db_path],
                                         stdout=open(os.devnull, 'wb'),
                                         stderr=subprocess.STDOUT)
        assert self._process, 'mongod failed to start'

    def _stop_mongod(self):
        """End the mongo db process."""
        if self._process:
            self._process.terminate()
            self._process.wait()
            self._process = None

    def _connect(self):
        """Connect to mongo db."""
        if self._process and (not self._client or not self._db):
            for _ in range(3):
                try:
                    self._client = pymongo.MongoClient()
                except ConnectionFailure:
                    time.sleep(0.1)
                    continue
                else:
                    break
            if self._client:
                self._db = self._client.task_list

    def _disconnect(self):
        """Disconnect from mongo db."""
        self._db = None
        self._client = None

    def add(self, task: dict) -> int:
        """Add task dict to the db."""
        return self._db.task_list.insert_one(task).inserted_id

    def get(self, task_id: int) -> dict:
        """Return a task dict with the matching id."""
        task_dict = self._db.task_list.find_one({'_id': ObjectId(task_id)})
        task_dict['id'] = task_dict['_id']
        del task_dict['_id']
        return task_dict

    def list_tasks(self, owner: str) -> List[dict]:
        """Return a list of tasks."""
        return list(self._db.task_list.find())

    def count(self) -> int:
        """Return the number of tasks in the db."""
        return self._db.task_list.count()

    def update(self, task_id: int, task: dict) -> None:
        """Modify a task in the db."""
        self._db.tasks_list.update_one({'_id': ObjectId(task_id)}, task)

    def delete(self, task_id: int) -> None:
        """Remove the task from the db."""
        reply = self._db.task_list.delete_one({'_id': ObjectId(task_id)})
        if reply.deleted_count == 0:
            raise ValueError(f'id {task_id!r} not in task database')

    def delete_all(self):
        """Remove all tasks from db."""
        self._db.task_list.drop()

    def unique_id(self) -> int:
        """Return an integer that does not exist in the db."""
        return hash(ObjectId())

    def stop_tasks_db(self):
        """Disconnect from the db."""
        self._disconnect()
        self._stop_mongod()


def start_tasks_db(db_path: str) -> TasksDB_MongoDB:
    """Connect to db."""
    return TasksDB_MongoDB(db_path)
