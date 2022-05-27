import pytest

import tasks
from bson import ObjectId
from tasks import Task


def test_add_returns_valid_id(tasks_db):
    """add should return an integer or object id."""
    # GIVEN a task db

    # WHEN a new task is added
    new_task = Task('do something')

    # THEN returned task_id should be of type int
    task_id = tasks.add(new_task)
    assert isinstance(task_id, int) or isinstance(task_id, ObjectId)


@pytest.mark.smoke
def test_added_task_has_id_set(tasks_db):
    """task_id field should be set by tasks.add()"""
    # GIVEN a task db
    #   AND  a new task is added
    new_task = Task('sleep', owner='cat', done=True)
    task_id = tasks.add(new_task)

    # WHEN task is retrieved
    task_from_db = tasks.get(task_id)

    # THEN task_id_matches id field
    assert task_from_db.id == task_id


def test_add_increases_count(db_with_3_tasks):
    """Test that add affects task.count()."""
    # Given a db with 3 tasks
    # WHEN another task is added
    tasks.add(Task('fly'))

    # Then the count increases by 1
    assert tasks.count() == 4
