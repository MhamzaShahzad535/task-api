from sqlalchemy.orm import Session

import models
import schemas



# Get all tasks

def get_tasks(db: Session):

    return db.query(models.Task).all()



# Get one task

def get_task(db: Session, task_id: int):

    return (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )



# Create task

def create_task(db: Session, task: schemas.TaskCreate):

    new_task = models.Task(
        title=task.title,
        done=False
    )


    db.add(new_task)

    db.commit()

    db.refresh(new_task)


    return new_task



# Update task

def update_task(
    db: Session,
    task_id: int,
    updated_task: schemas.TaskUpdate
):

    task = get_task(db, task_id)


    if task is None:
        return None


    if updated_task.title is not None:
        task.title = updated_task.title


    if updated_task.done is not None:
        task.done = updated_task.done


    db.commit()

    db.refresh(task)


    return task



# Delete task

def delete_task(db: Session, task_id: int):

    task = get_task(db, task_id)


    if task is None:
        return None


    db.delete(task)

    db.commit()


    return task