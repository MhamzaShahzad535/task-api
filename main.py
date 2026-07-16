from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI()
class TaskCreate(BaseModel):
    title: str
    
class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
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
@app.get(
    "/",
    description="Returns information about this API"
)
def root():
    return{
        "name": "Task API",
        "version": "1.0.0",
        "endpoints": ["/tasks"]
    }
@app.get(
    "/health",
    description="Returns the health status of the API"
)
def health():
    return {
        "status": "ok"
    }
@app.get(
    "/tasks",
    description="Returns the list of tasks"
)
def get_tasks():
    return tasks

@app.get(
    "/tasks/{task_id}",
    description="Returns a specific task by its ID"
)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
@app.post(
    "/tasks",
    description="Creates a new task",
    status_code=201
)
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

@app.put(
    "/tasks/{task_id}",
    description="Updates a specific task by its ID"
)
def update_task(task_id: int, updated_task: TaskUpdate):

    for task in tasks:
        if task["id"] == task_id:

            if updated_task.title is not None:
                task["title"] = updated_task.title

            if updated_task.done is not None:
                task["done"] = updated_task.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
@app.delete(
    "/tasks/{task_id}",
    description="Deletes a specific task by its ID",
    status_code=204
)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] ==  task_id:
            tasks.remove(task)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )