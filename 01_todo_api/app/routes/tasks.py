from fastapi import APIRouter, HTTPException, Path
from app.database.connection import LocalSession
from app.schema.task_schema import CreateTask, UpdateTask
from sqlalchemy import text 
from datetime import datetime


router = APIRouter()

# Create A Task
@router.post('/tasks')
def create_task(task : CreateTask):
    db = LocalSession()
    query = text(
        """
            INSERT INTO task_table (title, description, priority, completed, created_at)
            VALUES ( :title, :description, :priority, :completed, :created_at)
        """
    )
    res = db.execute(query,
            {
                'title':task.title,
                'description': task.description,
                'priority': task.priority, 
                'completed': False,
                'created_at': datetime.now()
            }
    )
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
    if not all_tasks:
        return {
            'message': 'No Tasks Present',
            'tasks' : []
        }
    
    total_tasks = len(all_tasks)
    return {
            'message': f'{total_tasks} Tasks Present',
            'tasks' : all_tasks
        }



# Get A Single Task
@router.get('/tasks/{task_id}')
def get_one_task(task_id:int = Path(..., title='Task ID', description='Enter Task ID', example = 1 )):
    db = LocalSession()
    query = text(
        """
            SELECT * FROM task_table
            WHERE id = :id
        """
    )
    res = db.execute(query,
                { "id" : task_id}
    )
    task = res.fetchone()
    db.close()
    if not task:
        raise HTTPException (status_code=404, detail=f"Task with Task ID = {task_id} doesn't exists")

    return dict(task._mapping)



# Update A Task 
@router.put('/tasks/{task_id}')
def update_task(update_info : UpdateTask,
                task_id : int = Path(..., title='Task ID', description='Enter Task ID', example = 1 )):
    db = LocalSession()
    query = text(
        """
            UPDATE task_table
            SET 
                title = :title, 
                description = :description,
                priority = :priority,
                created_at = :created_at, 
                completed = :completed
            WHERE
                id = :id
        """
    )
    res = db.execute(query,
                {
                    'id' : task_id,
                    'title': update_info.title,
                    'description': update_info.description,
                    'priority': update_info.priority,
                    'completed' : update_info.completed,
                    'created_at': datetime.now()
                }
    )
    db.commit()
    if res.rowcount == 0:
        db.close()
        raise HTTPException(status_code=404, detail=f"Update Unsucessful. Task with Task ID = {task_id} doesn't exists")

    db.close()
    return {
        'message': f'Task with Task ID = {task_id} Updated Successfully'
    }



# Delete A Task
@router.delete('/tasks/{task_id}')
def delete_task(task_id : int = Path(..., title='Task ID', description='Enter Task ID', example = 1 )):
    db = LocalSession()
    query = text(
        """
            DELETE FROM task_table
            WHERE id = :id
        """
    )
    res = db.execute(query, 
            {
                'id' : task_id
            }
    )
    db.commit()
    if res.rowcount == 0:
        db.close()
        raise HTTPException(status_code=404, detail = f"Deletion Unsuccessful. Task with Task ID = {task_id} doesn't exists")
    
    # if Table is empty -> reset id to 0
    count_query = text(
        "SELECT COUNT(*) FROM task_table"
    )
    count_res = db.execute(count_query)
    total_remaining_rows = count_res.fetchone()[0]
    if total_remaining_rows == 0:
        reset_id_query = text(
            "ALTER TABLE task_table AUTO_INCREMENT  = 1"
        )
        db.execute(reset_id_query)
        db.commit()
    
    db.close()
    return {
        'message': f'Task with Task ID = {task_id} Deleted Successfully'
    }



# Mark A Task Status Complete
@router.patch('/tasks/{task_id}')
def mark_complete(task_id : int = Path(..., title='Task ID', description='Enter Task ID', example = 1 )):
    db = LocalSession()
    query = text(
        """UPDATE task_table
        SET completed = TRUE
        WHERE id = :id"""
    )
    res = db.execute(query, {'id': task_id})
    db.commit()
    if res.rowcount == 0:
        db.close()
        raise HTTPException(status_code=404, detail=f"Mark Complete Unsuccessful. Task with Task ID = {task_id} doesn't exists")

    db.close()
    return {
        'message': f"Task with Task ID = {task_id} Marked Completed"
    }