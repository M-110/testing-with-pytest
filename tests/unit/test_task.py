"""Test the Task data type."""

from collections import namedtuple

from tasks import Task


def test_asdict():
    """asdict() should return a dictionary."""
    t_task = Task('do something', 'okay', True, 21)
    t_dict = t_task._asdict()
    expected = dict(summary='do something',
                    owner='okay',
                    done=True,
                    id=21)
    assert t_dict == expected


def test_replace():
    """Replace should change passed in fields."""
    t_before = Task('finish book', 'brian', False)
    t_after = t_before._replace(id=10, done=True)
    t_expected = Task('finish book', 'brian', True, 10)
    assert t_after == t_expected


def test_defaults():
    """Using no parameters, invoke defaults."""
    t1 = Task()
    t2 = Task(None, None, False, None)
    assert t1 == t2


def test_member_access():
    """Check the field functionality."""
    t = Task('buy milk', 'brian')
    assert t.summary == 'buy milk'
    assert t.owner == 'brian'
