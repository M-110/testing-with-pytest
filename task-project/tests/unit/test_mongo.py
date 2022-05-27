"""Test the opening and closing of mongo connections."""
from tasks import tasksdb_pymongo as mongo


def test_stopping_mongo(tmpdir):
    """Test stopping mongo without exceptions."""
    db = mongo.start_tasks_db(tmpdir)
    db.stop_tasks_db()


def test_mongo_unique(tmpdir):
    db = mongo.start_tasks_db(tmpdir)
    a = db.unique_id()
    b = db.unique_id()
    assert a != b


