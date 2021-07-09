from collections import namedtuple
from typing import List, Literal, Optional

Task = namedtuple('Task', 'summary owner done id',
                  defaults=(None, None, False, None))


class TasksException(Exception):
    """A tasks error has occurred."""


class UninitializedDatabase(TasksException):
    """Call tasks.start_tasks_db() before other functions."""


def add(task: Task) -> int:
    if not isinstance(task, Task):
        raise TypeError('task must be a Task object')


def get(task_id: int) -> Task:
    if not isinstance(task_id, int):
        raise TypeError('task_id must be an integer')


def list_tasks(owner: Optional[str] = None) -> List[Task]:
    if not isinstance(owner, str):
        raise TypeError('owner must be a string')


def count() -> int:
    ...


def update(task_id: int, task: Task) -> None:
    ...


def delete(task_id: int) -> None:
    ...


def delete_all() -> None:
    ...


def unique_id() -> int:
    ...


def start_tasks_db(db_path: str, db_type: Literal['tiny', 'mongo']) -> None:
    if db_type not in ['tiny', 'mongo']:
        raise ValueError("db_type must be 'tiny' or 'mongo'")


def stop_tasks_db() -> None:
    ...
