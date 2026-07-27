from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3



app = FastAPI()



DATABASE = "tasks.db"



def get_connection():
    conn = sqlite3.connect(DATABASE)

    
    conn.row_factory = sqlite3.Row

    return conn



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




create_database()
insert_initial_tasks()




class TaskCreate(BaseModel):
    title: str




class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None



@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "2.0.0",
        "database": "SQLite"
    }



@app.get("/health")
def health():
    return {
        "status": "ok"
    }