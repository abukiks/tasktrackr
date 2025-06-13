from fastapi import FastAPI, HTTPException
from app.models import Task, TaskCreate

app = FastAPI()

# In-memory DB
tasks = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Welcome to TaskTrackr 🚀"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, title=task.title, completed=task.completed)
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = Task(id=task_id, title=updated_task.title, completed=updated_task.completed)
            return tasks[i]
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")

