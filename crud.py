from sqlalchemy.orm import Session
from src import models
from src.schemas import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)

    if not db_task:
        return None

    if task.title is not None:
        db_task.title = task.title

    if task.description is not None:
        db_task.description = task.description

    if task.completed is not None:
        db_task.completed = task.completed

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)

    if not db_task:
        return None

    db.delete(db_task)
    db.commit()

    return db_task