"""Test the update function."""
import pytest

import tasks
from tasks import Task


def test_update(tasks_db):
    """Test updating a task."""
    task_a = Task('Hello')
    task_id = tasks.add(task_a)
    task_b = Task('Goodbye')
    tasks.update(task_id, task_b)
    task_b = Task('Goodbye', id=task_id)
    assert tasks.get(task_id) == task_b


def test_update_not_int(tasks_db):
    """Test that update raises an error when given a non-int id"""
    with pytest.raises(TypeError):
        tasks.update('dog', 'cat')


def test_update_not_task(tasks_db):
    """Test that update raises an error when given a non-int id"""
    with pytest.raises(TypeError):
        tasks.update(1, 'cat')
