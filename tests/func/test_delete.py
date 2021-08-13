"""Test deleting object from db"""
import pytest

import tasks
from tasks import Task


def test_delete(tasks_db):
    """Test deleting a task."""
    task_id = tasks.add(Task('Hello'))
    tasks.delete(task_id)
    with pytest.raises(ValueError):
        tasks.get(task_id)


def test_delete_raises(tasks_db):
    task_id = tasks.add(Task('Hello'))
    tasks.delete(task_id)
    with pytest.raises((ValueError, KeyError)):
        tasks.delete(task_id)
