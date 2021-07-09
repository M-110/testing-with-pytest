"""Use the Task type to show test failures."""

from tasks import Task


def test_task_equality():
    """Different tasks should not be equal"""
    t1 = Task('run', 'doug')
    t2 = Task('walk', 'doug')
    
    assert t1 != t2
    

def test_dict_equality():
    """Different dicts should not be equal."""
    t1_dict = Task('run', 'doug')._asdict()
    t2_dict = Task('walk', 'doug')._asdict()
    assert t1_dict != t2_dict
