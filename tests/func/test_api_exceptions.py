"""Test api functions return exceptions when given bad parameters."""

import pytest

import tasks


def test_add_raises():
    """Raise exception when parameter isn't a Task."""
    with pytest.raises(TypeError):
        tasks.add(task='Some string')
    

def test_start_tasks_db_raises():
    """Raises exception if the db isn't mongo or tiny."""
    with pytest.raises(ValueError) as info:
        tasks.start_tasks_db('my/path', 'mysql')
    message = info.value.args[0]
    assert message == "db_type must be 'tiny' or 'mongo'"
    
    
@pytest.mark.smoke
def test_list_raises():
    """Raises exception if owner is not a string."""
    with pytest.raises(TypeError):
        tasks.list_tasks(owner=500)


@pytest.mark.get
@pytest.mark.smoke
def test_get_raises():
    """Raises exception if task_id is not an integer."""
    with pytest.raises(TypeError):
        tasks.get(task_id=1.0)

