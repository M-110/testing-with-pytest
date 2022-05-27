"""Test the list_tasks function for the dbs"""
import tasks
from tasks import Task


def test_list_all(tasks_db):
    """Test list all."""
    my_task = Task('Hello', owner='Pycharm')
    your_task = Task('Goodbye', owner='Vscode')
    my_id = tasks.add(my_task)
    your_id = tasks.add(your_task)
    my_task = Task('Hello', owner='Pycharm', id=my_id)
    your_task = Task('Goodbye', owner='Vscode', id=your_id)
    all_tasks = tasks.list_tasks()
    assert (my_task in all_tasks) and (your_task in all_tasks)


def test_list_someone(tasks_db):
    """Test list with a specific owner."""
    my_task = Task('Hello', owner='Pycharm')
    my_id = tasks.add(my_task)
    my_task = Task('Hello', owner='Pycharm', id=my_id)
    pycharm_tasks = tasks.list_tasks('Pycharm')
    assert my_task in pycharm_tasks
