from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3


# Create FastAPI app
app = FastAPI()


# Database file
DATABASE = "tasks.db"



# Create connection to SQLite
def get_connection():

    conn = sqlite3.connect(DATABASE)

    # Allows access using column names
    conn.row_factory = sqlite3.Row

    return conn



# Create database table
def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL
    )
    """)

    conn.commit()

    conn.close()



# Insert example tasks only once
def insert_initial_tasks():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")

    count = cursor.fetchone()[0]


    if count == 0:

        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            ("Study FastAPI", False)
        )


        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            ("Buy milk", True)
        )


        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            ("Walk the dog", False)
        )


    conn.commit()

    conn.close()



# Run database setup
create_database()
insert_initial_tasks()



# Pydantic models

class TaskCreate(BaseModel):
    title: str



class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None




# Root endpoint
@app.get("/")
def root():

    return {
        "name": "Task API",
        "version": "2.0.0",
        "database": "SQLite"
    }



# Health endpoint
@app.get("/health")
def health():

    return {
        "status": "ok"
    }



# GET all tasks
@app.get("/tasks")
def get_tasks():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()


    tasks = []


    for row in rows:

        tasks.append({
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        })


    return tasks




# GET one task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )


    row = cursor.fetchone()

    conn.close()


    if row is None:

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )


    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }




# CREATE task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if not task.title.strip():

        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """,
        (task.title, False)
    )


    task_id = cursor.lastrowid


    conn.commit()

    conn.close()


    return {
        "id": task_id,
        "title": task.title,
        "done": False
    }




# UPDATE task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    conn = get_connection()

    cursor = conn.cursor()


    # Check task exists
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )


    row = cursor.fetchone()


    if row is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )


    # Keep old values if not provided
    title = (
        updated_task.title
        if updated_task.title is not None
        else row["title"]
    )


    done = (
        updated_task.done
        if updated_task.done is not None
        else row["done"]
    )


    # Update database
    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (title, done, task_id)
    )


    conn.commit()

    conn.close()


    return {
        "id": task_id,
        "title": title,
        "done": bool(done)
    }