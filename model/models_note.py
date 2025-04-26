from sqlalchemy import Column, String, DateTime, ARRAY
from sqlalchemy.sql import func
from db_connect import Base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class NoteDB(Base):
    __tablename__ = 'note1'
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    title = Column(String)
    description = Column(String)

class NoteSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    description: str
    
    class Config:
        from_attributes = True 

