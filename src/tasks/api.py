﻿from bson.objectid import ObjectId
from collections import namedtuple
from typing import List, Literal, Optional, Union

import tasks.tasksdb_tinydb
import tasks.tasksdb_pymongo

Task = namedtuple('Task', 'summary owner done id',
                  defaults=(None, None, False, None))

Database = Union[tasks.tasksdb_tinydb.TasksDB_TinyDB,
                 tasks.tasksdb_pymongo.TasksDB_MongoDB]


class TasksException(Exception):
    """A tasks error has occurred."""


class UninitializedDatabase(TasksException):
    """Call tasks.start_tasks_db() before other functions."""


def add(task: Task) -> Union[int, ObjectId]:
    """Add a task to the tasks database."""
    if not isinstance(task, Task):
        raise TypeError('task must be a Task object')
    task_id = _tasks_db.add(task._asdict())
    return task_id


def get(task_id: Union[int, ObjectId]) -> Task:
    if not (isinstance(task_id, int) or isinstance(task_id, ObjectId)):
        raise TypeError('task_id must be an integer or ObjectId')
    if _tasks_db is None:
        raise UninitializedDatabase
    task_dict = _tasks_db.get(task_id)
    print(task_dict)
    return Task(**task_dict)


def list_tasks(owner: Optional[str] = None) -> List[Task]:
    if not isinstance(owner, str):
        raise TypeError('owner must be a string')


def count() -> int:
    if _tasks_db is None:
        raise UninitializedDatabase
    return _tasks_db.count()


def update(task_id: int, task: Task) -> None:
    if not isinstance(task_id, int):
        raise TypeError('task_id must be an integer')
    if not isinstance(task, Task):
        raise TypeError('task must be a Task')


def delete(task_id: int) -> None:
    ...


def delete_all() -> None:
    """Remove all tasks from the db."""
    if _tasks_db is None:
        raise UninitializedDatabase
    _tasks_db.delete_all()


def unique_id() -> Union[int, ObjectId]:
    """Return an integer that does not exist in the the db."""
    if _tasks_db is None:
        raise UninitializedDatabase
    return _tasks_db.unique_id()


_tasks_db: Optional[Database] = None


def start_tasks_db(db_path: str, db_type: Literal['tiny', 'mongo']) -> None:
    """Connect to the db."""
    if db_type not in ['tiny', 'mongo']:
        raise ValueError("db_type must be 'tiny' or 'mongo'")
    global _tasks_db
    if db_type == 'tiny':
        _tasks_db = tasks.tasksdb_tinydb.start_tasks_db(db_path)
    else:
        _tasks_db = tasks.tasksdb_pymongo.start_tasks_db(db_path)


def stop_tasks_db() -> None:
    """Disconnect from the db."""
    global _tasks_db
    if _tasks_db is not None:
        _tasks_db.stop_tasks_db()
    _tasks_db = None
