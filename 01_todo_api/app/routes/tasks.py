from fastapi import APIRouter
from app.database.connection import LocalSession
from app.schema.task_schema import CreateTask
from sqlalchemy import text 


router = APIRouter()

# Create A Task
@router.post('/tasks')
def create_task(task : CreateTask):
    db = LocalSession()
    query = text(
        """
            INSERT INTO task_table (title, description, priority)
            VALUES ( :title, :description, :priority)
        """
    )
    res = db.execute(query,
            {
                'title':task.title,
                'description': task.description,
                'priority': task.priority
            })
    db.commit()
    created_task_id = res.lastrowid
    db.close()
    return {
        'message': "Task Created Successfully",
        'task_id': created_task_id
    }


# Get All Tasks
@router.get('/tasks')
def get_all_task():
    db = LocalSession()
    query = text(
        'SELECT* FROM task_table'
    )
    res = db.execute(query)
    all_tasks_in_ROWS = res.fetchall() # DB row
    all_tasks = [dict(db_row._mapping) for db_row in all_tasks_in_ROWS]
    db.close()
    return all_tasks

# Get A Single Task
@router.get('/tasks/{task_id}')
def get_one_task():
    pass


# Update A Task 
@router.put('/tasks/{task_id}')
def update_task():
    pass

# Delete A Task
@router.delete('/tasks/{task_id}')
def delete_task():
    pass

# Mark A Task Status Complete
@router.patch('/tasks/{task_id}')
def mark_complete():
    pass