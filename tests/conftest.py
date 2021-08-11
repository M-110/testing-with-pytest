import pytest

import tasks
from tasks import Task

# Plugin basically:


def pytest_addoption(parser):
    """Turn nice features on with --nice option."""
    group = parser.getgroup('nice')
    group.addoption('--nice', action='store_true',
                    help='nice: turn failures into opportunities')


def pytest_report_header(config):
    """Thank the tester."""
    if config.getoption('--nice'):
        return "Thanks for running the tests!"


def pytest_report_teststatus(report, config):
    """Turn failures into opportunities."""
    nice = config.getoption('--nice')
    if report.when == 'call' and report.failed and nice:
        return report.outcome, 'O', 'OPPORTUNITY for improvement'


@pytest.fixture(scope='session', params=['tiny', 'mongo'])
def tasks_db_session(tmpdir_factory, request):
    """Connect to a db before tests, then disconnect after."""
    temp_dir = tmpdir_factory.mktemp('temp')
    tasks.start_tasks_db(str(temp_dir), request.param)
    yield
    tasks.stop_tasks_db()


@pytest.fixture()
def tasks_db(tasks_db_session):
    """An empty tasks db."""
    tasks.delete_all()


@pytest.fixture(scope='session')
def tasks_just_a_few():
    """Returns three tasks."""
    return (Task('Write code', 'Brian', True),
            Task('Code review', 'Katie', False),
            Task('Fix code', 'Michelle', False))


@pytest.fixture(scope='session')
def tasks_multi_per_owner():
    """Returns 10 tasks with three different owners."""
    return (Task('Bake cake', 'Raphael'),
            Task('Sing', 'Raphael'),
            Task('Use an emoji', 'Raphael'),
            Task('Move to Berlin', 'Raphael'),

            Task('Create', 'Michelle'),
            Task('Inspire', 'Michelle'),
            Task('Encourage', 'Michelle'),

            Task('Do a handstand', 'Daniel'),
            Task('Write some books', 'Daniel'),
            Task('Eat ice cream', 'Daniel'))


@pytest.fixture()
def db_with_3_tasks(tasks_db, tasks_just_a_few):
    """Connects to db with 3 tasks added."""
    for task in tasks_just_a_few:
        tasks.add(task)


@pytest.fixture()
def db_with_multi_per_owner(tasks_db, tasks_multi_per_owner):
    """Connected to db with 9 tasks between 3 owners."""
    for task in tasks_multi_per_owner:
        tasks.add(task)
