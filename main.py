from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row


# Create FastAPI app
app = FastAPI()


# Load .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")



# Create PostgreSQL connection
def get_connection():

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )



# Create database table
def create_database():

    conn = get_connection()

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



# Insert example tasks only once
def insert_initial_tasks():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM tasks"
    )


    count = cursor.fetchone()["count"]


    if count == 0:

        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            """,
            ("Study FastAPI", False)
        )


        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            """,
            ("Buy milk", True)
        )


        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            """,
            ("Walk the dog", False)
        )


    conn.commit()

    conn.close()



# Setup database when app starts
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
        "version": "3.0.0",
        "database": "PostgreSQL"
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


    cursor.execute(
        "SELECT * FROM tasks"
    )


    tasks = cursor.fetchall()


    conn.close()


    return tasks





# GET task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )


    task = cursor.fetchone()


    conn.close()


    if task is None:

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )


    return task





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
        VALUES (%s, %s)
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





# UPDATE task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )


    task = cursor.fetchone()


    if task is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
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
        SET title = %s, done = %s
        WHERE id = %s
        """,
        (title, done, task_id)
    )


    conn.commit()

    conn.close()



    return {
        "id": task_id,
        "title": title,
        "done": done
    }





# DELETE task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )


    task = cursor.fetchone()


    if task is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )



    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )


    conn.commit()

    conn.close()


    return