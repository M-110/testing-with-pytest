import pytest

import tasks

from tasks import Task


def test_add_1():
    """tasks.get() using id returned from add works."""
    task = Task('breathe', 'Brian', True)
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)


@pytest.mark.parametrize('task',
                         [Task('sleep', done=True),
                          Task('wake up', 'Angel'),
                          Task('run', 'CAPTAIN', False),
                          Task('walk')])
def test_add_2(task):
    """tasks.get() using id returned from add works."""
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)


@pytest.mark.parametrize('task',
                         [('sleep', None, True),
                          ('wake up', 'Angel'),
                          ('run', 'CAPTAIN', False),
                          ('walk')])
def test_add_3(task):
    """tasks.get() using id returned from add works."""
    task_id = tasks.add(Task(*task))
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, Task(*task))


@pytest.mark.parametrize('summary, owner, done',
                         [('sleep', None, True),
                          ('wake up', 'Angel', False),
                          ('run', 'CAPTAIN', False),
                          ('walk', 'Candy', False)])
def test_add_4(summary, owner, done):
    """tasks.get() using id returned from add works."""
    task_id = tasks.add(Task(summary, owner, done))
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, Task(summary, owner, done))


tasks_to_try = (Task('sleep', done=True),
                Task('wake', 'brian'),
                Task('wake', 'brian'),
                Task('Sleep', 'BRIAN', True),
                Task('Exercise', 'BriaN', False))


@pytest.mark.parametrize('task', tasks_to_try, ids=str)
def test_add_4(task):
    """tasks.get() using id returned from add works."""
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)


def equivalent(t1, t2):
    """Check two tasks for equivalence."""
    return ((t1.summary == t2.summary) and
            (t1.owner == t2.owner) and
            t1.done == t2.done)


@pytest.mark.parametrize('task', tasks_to_try, ids=str)
class TestAdd:
    """Parameterize and test class"""
    
    def test_eq(self, task):
        """Test id is correct"""
        task_id = tasks.add(task)
        t_from_db = tasks.get(task_id)
        
        assert equivalent(t_from_db, task)
        
    def test_valid_id(self, task):
        """Test the same thing above again"""
        task_id = tasks.add(task)
        t_from_db = tasks.get(task_id)
        assert t_from_db.id == task_id


@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    """Connect to db before testing, disconnect after."""
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    yield
    tasks.stop_tasks_db()
