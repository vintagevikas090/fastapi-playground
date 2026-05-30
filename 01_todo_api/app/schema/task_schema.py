from pydantic import BaseModel, Field
from typing import Annotated, Literal

class CreateTask(BaseModel):
    title : Annotated[str, Field(
        min_length=3, title = 'Task Title', 
        description='Enter the Title Name for the Task(minimum 5 Characters)', 
        example = 'GenAI Seminar'
    )]

    description : Annotated[str, Field(
        min_length=10, title='Task Description', 
        description="Enter Some Description for task (minimum 10 Characters)",
        example = 'Attend GenAI Seminar on 15 June at 5:00 PM'
    )]

    priority : Annotated[Literal['Low', 'Medium', 'High'], Field(
        title = 'Task Priority', 
        description='Enter Task Priority(Low, High, Medium)',
        example = 'Low'
    )]


class UpdateTask(BaseModel):
    title : Annotated[str, Field(
        min_length=3, title = 'Task Title', 
        description='Enter the Title Name for the Task(minimum 5 Characters)', 
        example = 'GenAI Seminar'
    )]

    description : Annotated[str, Field(
        min_length=10, title='Task Description', 
        description="Enter Some Description for task (minimum 10 Characters)",
        example = 'Attend GenAI Seminar on 15 June at 5:00 PM'
    )]

    priority : Annotated[Literal['Low', 'Medium', 'High'], Field(
        title = 'Task Priority', 
        description='Enter Task Priority(Low, High, Medium)',
        example = 'Low'
    )]

    completed: Annotated[bool, Field(
        title="Task Status",
        description="Task completion status"
    )
    ] = False