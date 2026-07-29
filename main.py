from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import get_connection


app = FastAPI()


# -----------------------------
# Database setup
# -----------------------------

def create_database():

    print("Connecting to database...")

    conn = get_connection()

    print("Database connected!")

    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)


    conn.commit()
    conn.close()

    print("Table created!")



def insert_initial_tasks():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) AS count FROM tasks"
    )


    count = cursor.fetchone()["count"]


    if count == 0:

        cursor.execute(
            """
            INSERT INTO tasks(title, done)
            VALUES(%s,%s)
            """,
            ("Study FastAPI", False)
        )


        cursor.execute(
            """
            INSERT INTO tasks(title, done)
            VALUES(%s,%s)
            """,
            ("Buy milk", True)
        )


        cursor.execute(
            """
            INSERT INTO tasks(title, done)
            VALUES(%s,%s)
            """,
            ("Walk the dog", False)
        )


    conn.commit()
    conn.close()

    print("Initial tasks checked!")



@app.on_event("startup")
def startup_event():

    print("Starting database setup...")

    try:
        create_database()
        print("Database table ready!")

        insert_initial_tasks()
        print("Initial tasks checked!")

    except Exception as e:
        print("DATABASE ERROR:")
        print(e)
        raise e
# -----------------------------
# Models
# -----------------------------


class TaskCreate(BaseModel):
    title: str



class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None



# -----------------------------
# Routes
# -----------------------------


@app.get("/")
def root():

    return {
        "name": "Task API",
        "version": "3.0.0",
        "database": "PostgreSQL"
    }



@app.get("/health")
def health():

    return {
        "status": "ok"
    }



@app.get("/tasks")
def get_tasks():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks"
    )

    tasks = cursor.fetchall()

    conn.close()

    return tasks



@app.get("/tasks/{task_id}")
def get_task(task_id:int):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM tasks WHERE id=%s",
        (task_id,)
    )


    task = cursor.fetchone()

    conn.close()


    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return task



@app.post("/tasks", status_code=201)
def create_task(task:TaskCreate):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO tasks(title, done)
        VALUES(%s,%s)
        RETURNING id
        """,
        (task.title, False)
    )


    task_id = cursor.fetchone()["id"]


    conn.commit()

    conn.close()


    return {
        "id": task_id,
        "title": task.title,
        "done": False
    }



@app.put("/tasks/{task_id}")
def update_task(task_id:int, updated_task:TaskUpdate):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM tasks WHERE id=%s",
        (task_id,)
    )


    task = cursor.fetchone()


    if task is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    title = (
        updated_task.title
        if updated_task.title is not None
        else task["title"]
    )


    done = (
        updated_task.done
        if updated_task.done is not None
        else task["done"]
    )


    cursor.execute(
        """
        UPDATE tasks
        SET title=%s, done=%s
        WHERE id=%s
        """,
        (title, done, task_id)
    )


    conn.commit()

    conn.close()


    return {
        "id":task_id,
        "title":title,
        "done":done
    }



@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id:int):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id=%s
        RETURNING id
        """,
        (task_id,)
    )


    deleted = cursor.fetchone()


    conn.commit()

    conn.close()


    if deleted is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return