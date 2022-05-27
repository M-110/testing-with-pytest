"""Database wrapper for TinyDB"""
from typing import List

import tinydb


class TasksDB_TinyDB:
    """Wrapper class for TinyDB."""
    
    def __init__(self, db_path: str) -> None:
        """Connect to db."""
        self._db = tinydb.TinyDB(db_path + '/tasks_db.json')
        
    def add(self, task: dict) -> int:
        """Add task dict to the db."""
        task_id = self._db.insert(task)
        task['id'] = task_id
        self._db.update(task, doc_ids=[task_id])
        return task_id
    
    def get(self, task_id: int) -> dict:
        """Return a task dict with the matching id."""
        task = self._db.get(doc_id=task_id)
        if task is None:
            raise ValueError('Could not find task')
        return task
    
    def list_tasks(self, owner: str) -> List[dict]:
        """Return a list of tasks."""
        if owner is None:
            return self._db.all()
        return self._db.search(tinydb.Query().owner == owner)
    
    def count(self) -> int:
        """Return the number of tasks in the db."""
        return len(self._db)
    
    def update(self, task_id: int, task: dict) -> None:
        """Modify a task in the db."""
        self._db.update(task, doc_ids=[task_id])
        
    def delete(self, task_id: int) -> None:
        """Remove the task from the db."""
        self._db.remove(doc_ids=[task_id])
        
    def delete_all(self):
        """Remove all tasks from db."""
        self._db.truncate()
        
    def unique_id(self) -> int:
        """Return an integer that does not exist in the db."""
        i = 1
        while self._db.contains(doc_id=i):
            i += 1
        return i
    
    def stop_tasks_db(self):
        """Disconnect from the db."""
        self._db.close()
        

def start_tasks_db(db_path: str) -> TasksDB_TinyDB:
    """Connect to db."""
    return TasksDB_TinyDB(db_path)
