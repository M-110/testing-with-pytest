"""More task adding variety tests using parametrized fixtures."""
import pytest

import tasks
from tasks import Task

tasks_to_try = (Task('sleep', done=True),
                Task('wake', 'brian'),
                Task('brathe', 'BRIAN', True),
                Task('exercise', 'BrIaN', False))

tasks_ids = [repr(task) for task in tasks_to_try]


def equivalent(t1, t2):
    """Check two tasks are equal."""
    return ((t1.summary == t2.summary) and
            (t1.owner == t2.owner) and
            (t1.done == t2.done))


@pytest.fixture(params=tasks_to_try, ids=tasks_ids)
def a_task(request):
    """Tasks without ids."""
    return request.param


def test_add_a(tasks_db, a_task):
    """Using a_task fixtures."""
    task_id = tasks.add(a_task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, a_task)


def id_func(fixture_value):
    """Function for generating ids"""
    return repr(fixture_value)


@pytest.fixture(params=tasks_to_try, ids=id_func)
def c_task(request):
    """Using a function (id_func) to generate ids."""
    return request.param


def test_add_c(tasks_db, c_task):
    """Use fixture with generated id names."""
    task_id = tasks.add(c_task)
    t_from_db = tasks.get(task_id)
    assert equivalent(c_task, t_from_db)
