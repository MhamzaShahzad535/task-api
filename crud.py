from sqlalchemy.orm import Session

from models import Task
from schemas import TaskCreate



def get_tasks(db: Session):

    return db.query(Task).all()



def get_task(db: Session, task_id: int):

    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )



def create_task(db: Session, task: TaskCreate):

    new_task = Task(
        title=task.title,
        done=False
    )


    db.add(new_task)

    db.commit()

    db.refresh(new_task)


    return new_task