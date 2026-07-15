from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI()
class TaskCreate(BaseModel):
    title: str
tasks = [
    {
        "id": 1,
        "title": "Study FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Buy milk",
        "done":True
    },
    {
        "id": 3,
        "title": "Walk the dog",
        "done": False
    }
]
@app.get("/")
def root():
    return{
        "name": "Task API",
        "version": "1.0.0",
        "endpoints": ["/tasks"]
    }
@app.get("/health")
def health():
    return {
        "status": "ok"
    }
@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
@app.post("/tasks",status_code=201)
def create_task(task: TaskCreate):
    
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )
    new_task = {
        "id": len(tasks) +1,
        "title": task.title,
        "done" : False
    }
    tasks.append(new_task)
    return new_task