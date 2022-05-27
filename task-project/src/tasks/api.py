from bson.objectid import ObjectId
from collections import namedtuple
from functools import wraps
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


def require_db(func):
    """Decorator for checking the db is connected."""

    @wraps(func)
    def inner(*args, **kwargs):
        """Check if db is connected."""
        if _tasks_db is None:
            raise UninitializedDatabase('Database not connected')
        return func(*args, **kwargs)

    return inner


@require_db
def add(task: Task) -> int:
    """Add a task to the tasks database."""
    if not isinstance(task, Task):
        raise TypeError('task must be a Task object')
    if task.summary is None:
        raise ValueError('Summary required for a task')
    if not isinstance(task.done, bool):
        raise ValueError('done must be a bool')
    task_id = _tasks_db.add(task._asdict())
    return task_id


@require_db
def get(task_id: int) -> Task:
    if not isinstance(task_id, int):
        raise TypeError('task_id must be an integer or ObjectId')
    task_dict = _tasks_db.get(task_id)
    print(task_dict)
    return Task(**task_dict)


@require_db
def list_tasks(owner: Optional[str] = None) -> List[Task]:
    """List all the tasks of a given owner. If owner is not provided,
    all tasks will be returned."""
    if owner and not isinstance(owner, str):
        raise TypeError('owner must be a string')
    return [Task(**t) for t in _tasks_db.list_tasks(owner)]


@require_db
def count() -> int:
    """Return number of tasks in the db."""
    return _tasks_db.count()


@require_db
def update(task_id: int, task: Task) -> None:
    """Update task at task id with new task."""
    if not isinstance(task_id, int):
        raise TypeError('task_id must be an integer')
    if not isinstance(task, Task):
        raise TypeError('task must be a Task')
    current_task = _tasks_db.get(task_id)
    updates = task._asdict()
    for field in task._fields:
        if field != 'id' and updates[field] is not None:
            current_task[field] = updates[field]
    _tasks_db.update(task_id, current_task)


@require_db
def delete(task_id: int) -> None:
    """Delete a task from the db."""
    _tasks_db.delete(task_id)


@require_db
def delete_all() -> None:
    """Remove all tasks from the db."""
    _tasks_db.delete_all()


@require_db
def unique_id() -> int:
    """Return an integer that does not exist in the the db."""
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
