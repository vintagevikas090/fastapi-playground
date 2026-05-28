from pydantic import BaseModel

class CreateTask(BaseModel):
    title : str
    description : str
    priority : str


class UpdateTask(BaseModel):
    title : str
    description : str
    priority : str
    completed : bool