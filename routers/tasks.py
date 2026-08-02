from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas

from database import get_db


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



@router.get("/")
def read_tasks(
    db: Session = Depends(get_db)
):

    return crud.get_tasks(db)



@router.get("/{task_id}")
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



@router.post("/", status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):

    return crud.create_task(
        db,
        task
    )



@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):

    updated = crud.update_task(
        db,
        task_id,
        task
    )


    if updated is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return updated



@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    deleted = crud.delete_task(
        db,
        task_id
    )


    if deleted is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return {
        "message": "Task deleted"
    }