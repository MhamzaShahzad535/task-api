# Task API

A CRUD API built with FastAPI and SQLite.

## Description

This project is a task management API built using FastAPI.

It demonstrates the four CRUD operations:

* Create tasks
* Read tasks
* Update tasks
* Delete tasks

The API uses PostgreSQL running in Docker.
Data persists using a Docker volume, so tasks remain available after restarting the application or database container.

## Running with Docker

Start PostgreSQL:

docker compose up -d

Run the API:

uvicorn main:app --reload

## Technologies

* Python 3.10+
* FastAPI
* Uvicorn
* SQLite

## Database

This project uses SQLite because it is lightweight, requires no separate database server, and stores all data in a single database file.

The database file is:

```
tasks.db
```

The application automatically:

* Creates the database if it does not exist
* Creates the `tasks` table
* Inserts three example tasks on the first run only

## Installation

Clone the repository:

```bash
git clone https://github.com/MhamzaShahzad535/task-api.git
```

Go into the project folder:

```bash
cd task-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint           | Description       |
| ------ | ------------------ | ----------------- |
| GET    | `/tasks`           | Get all tasks     |
| GET    | `/tasks/{task_id}` | Get a task by ID  |
| POST   | `/tasks`           | Create a new task |
| PUT    | `/tasks/{task_id}` | Update a task     |
| DELETE | `/tasks/{task_id}` | Delete a task     |

## Example SQL Queries

Get all tasks:

```sql
SELECT * FROM tasks;
```

Show completed tasks:

```sql
SELECT * FROM tasks WHERE done = 1;
```

Count all tasks:

```sql
SELECT COUNT(*) FROM tasks;
```

## Database Screenshot

The SQLite database was inspected using DB Browser for SQLite.

![SQLite Database](sqlite-screenshot.png)
