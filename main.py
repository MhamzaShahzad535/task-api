from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


# Create FastAPI app
app = FastAPI()


# Database file name
DATABASE = "tasks.db"


# Connect to SQLite database
def get_connection():
    conn = sqlite3.connect(DATABASE)

    # Allows us to access columns using names
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



# Insert example tasks only when database is empty
def insert_initial_tasks():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")

    count = cursor.fetchone()[0]


    if count == 0:

        cursor.execute("""
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """, ("Study FastAPI", False))


        cursor.execute("""
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """, ("Buy milk", True))


        cursor.execute("""
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """, ("Walk the dog", False))


    conn.commit()

    conn.close()



# Run database setup
create_database()
insert_initial_tasks()



# Models
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



# Get all tasks from database
@app.get("/tasks")
def get_tasks():

    conn = get_connection()

    cursor = conn.cursor()

    # SQL query
    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()


    # Convert SQLite rows into JSON format
    tasks = []

    for row in rows:

        tasks.append({
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        })


    return tasks