from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database.connection import engine
from datetime import datetime


Base = declarative_base()

class Task(Base):
    __tablename__ = 'task_table'

    id = Column(Integer, primary_key=True, index = True)
    title = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)
    priority = Column(String(10), default='Medium')
    completed = Column(Boolean, default = False)
    created_at = Column(DateTime, nullable= False, default = datetime.now())

Base.metadata.create_all(bind = engine)