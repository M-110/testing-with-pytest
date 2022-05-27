import pytest

import tasks

from tasks import Task


def test_count():
    """Count should be 3 after adding 3 tasks."""
    tasks.add(Task('Buy apple', 'Oranges', False))
    tasks.add(Task('Buy apple', 'Oranges', False))
    tasks.add(Task('Buy apple', 'Oranges', False))
    assert tasks.count() == 3


@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    """Connect to db before testing, disconnect after."""
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    yield
    tasks.stop_tasks_db()