from fastapi import FastAPI
from app.routes.tasks import router 
from app.database import tables

app = FastAPI()

@app.get('/')
def home():
    return {
        'message': 'To-Do API Running'
    }

app.include_router(router)
