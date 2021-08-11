import pytest

import tasks
from tasks import Task


@pytest.mark.xfail()
def test_unique_id_1():
    """Calling unique_id() twice should return different values."""
    # GIVEN a task db
    # WHEN unique_id is called twice
    id_1 = tasks.unique_id()
    id_2 = tasks.unique_id()
    # THEN the ids should be equal
    assert id_1 != id_2


def test_unique_id_2():
    """unique_id() should return asn unused id"""
    # GIVEN a task db
    
    # WHEN four tasks are added and their ids are stored
    ids = []
    ids.append(tasks.add(Task('one')))
    ids.append(tasks.add(Task('two')))
    ids.append(tasks.add(Task('three')))
    ids.append(tasks.add(Task('four')))
    
    #   AND an id is retrieved from unique_id()
    unique = tasks.unique_id()
    
    # THEN the unique id should be different from the added ids.
    assert unique not in ids


@pytest.mark.xfail()
def test_unique_id_is_a_duck():
    """unique_id should not produce a duck."""
    # GIVEN a task db
    # WHEN an id is received an id from unique_id()
    uid = tasks.unique_id()
    # THEN the id should not be a duck
    assert uid == 'a duck'
    

@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    """Connect to db before testing, disconnect after."""
    # Setup: start db
    tasks.start_tasks_db(str(tmpdir), 'tiny')

    yield  # Testing occurs here

    # Teardown: stop db
    tasks.stop_tasks_db()
    