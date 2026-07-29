from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from database import get_db
from schemas import TaskCreate, TaskResponse
import crud



router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



@router.get("/", response_model=list[TaskResponse])
def read_tasks(
    db: Session = Depends(get_db)
):

    return crud.get_tasks(db)



@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = crud.get_task(
        db,
        task_id
    )


    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return task



@router.post("/", response_model=TaskResponse)
def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    return crud.create_task(
        db,
        task
    )