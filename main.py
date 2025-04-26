from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime
from db_connect import get_db
from model.models_note import NoteDB
from fastapi.middleware.cors import CORSMiddleware
from model.models_note import NoteDB, NoteSchema

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/src/assets"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoteServic:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_note(self, skip: int = 0, limit: int = 10):
        try:
            result = await self.db.execute(select(NoteDB).offset(skip).limit(limit))
            notes = result.scalars().all()
            return [NoteDB(id=note.id, created_at=note.created_at, title=note.title, description=note.description) for note in notes]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/", response_model=list[NoteSchema])
async def get_notes(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(NoteDB).offset(skip).limit(limit))
        notes = result.scalars().all()
        return notes  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)