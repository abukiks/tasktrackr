from fastapi import FastAPI, HTTPException
from app.database import database, engine, metadata
from app.models import tasks
from app.schemas import Task, TaskCreate

app = FastAPI()

metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def root():
    return {"message": "Welcome to TaskTrackr 🚀"}

@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    task = await database.fetch_one(query)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    query = tasks.insert().values(title=task.title, completed=task.completed)
    task_id = await database.execute(query)
    return {**task.dict(), "id": task_id}

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: TaskCreate):
    query = tasks.update().where(tasks.c.id == task_id).values(
        title=updated_task.title,
        completed=updated_task.completed
    )
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {**updated_task.dict(), "id": task_id}

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return

