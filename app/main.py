from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, database
from app.config import settings
import logging

from pydantic import BaseModel, ConfigDict
from typing import List
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modern FastAPI startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 TaskTrackr is starting up...")
    yield
    logger.info("🛑 TaskTrackr is shutting down...")

app = FastAPI(lifespan=lifespan)

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema
class TaskSchema(BaseModel):
    id: int
    title: str
    completed: bool = False

    model_config = ConfigDict(from_attributes=True)  # 👈 replaces orm_mode

@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": f"Welcome to {settings.APP_NAME}!"}

@app.get("/tasks", response_model=List[TaskSchema])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskSchema, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, updated: TaskSchema, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated.title
    task.completed = updated.completed
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
