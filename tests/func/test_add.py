import pytest

import tasks
from tasks import Task


def test_add_returns_valid_id():
    """add should return an integer."""
    # GIVEN a task db
    
    # WHEN a new task is added
    new_task = Task('do something')
    
    # THEN returned task_id should be of type int
    task_id = tasks.add(new_task)
    assert isinstance(task_id, int)
    

@pytest.mark.smoke
def test_added_task_has_id_set():
    """task_id field should be set by tasks.add()"""
    # GIVEN a task db
    #   AND  a new task is added
    new_task = Task('sleep', owner='cat', done=True)
    task_id = tasks.add(new_task)
    
    # WHEN task is retrieved
    task_from_db = tasks.get(task_id)
    
    # THEN task_id_matches id field
    assert task_from_db.id == task_id


@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    """Connect to db before testing, disconnect after."""
    # Setup: start db
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    
    yield  # Testing occurs here
    
    # Teardown: stop db
    tasks.stop_tasks_db()