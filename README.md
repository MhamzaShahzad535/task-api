# Task API

A CRUD API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Docker**.

## Description

This project is a task management REST API built using FastAPI.

It demonstrates the four CRUD operations:

- Create tasks
- Read tasks
- Update tasks
- Delete tasks

The API uses PostgreSQL as the database and SQLAlchemy as the ORM layer.

PostgreSQL runs inside a Docker container, and data persists using a Docker volume. This means tasks remain available even after restarting the application or database container.

---

## Technologies

- Python 3.10+
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Docker
- Pydantic

---

## Project Structure

```text
task-api/
│
├── main.py              # FastAPI application entry point
├── database.py          # Database connection and session management
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response schemas
├── crud.py              # Database CRUD operations
│
├── routers/
│   └── tasks.py         # Task API routes
│
├── docker-compose.yml   # PostgreSQL Docker configuration
├── .env                 # Environment variables
├── requirements.txt     # Project dependencies
└── README.md