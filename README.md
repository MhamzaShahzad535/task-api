# Task API

A secure Task Management API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Supabase Authentication**.

This project demonstrates:

- CRUD operations for tasks
- User authentication (Signup, Login, Logout)
- JWT token verification
- Protected API routes
- Swagger UI testing with Bearer Authentication
- Database integration using SQLAlchemy


## Features

- FastAPI backend
- PostgreSQL database
- SQLAlchemy ORM
- Supabase Auth integration
- JWT-based authentication
- Protected endpoints
- Swagger API documentation
- Environment variable configuration


# Technologies

- Python 3.10+
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Supabase Auth
- Swagger UI


# Project Structure

```
task-api/
│
├── routers/
│   ├── auth.py
│   ├── protected.py
│   ├── public.py
│   └── tasks.py
│
├── dependencies/
│   └── auth.py
│
├── database.py
├── models.py
├── schemas.py
├── supabase_client.py
├── main.py
├── .env
└── README.md
```


# Installation

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
pip install -r requirements.txt
```


# Environment Variables

Create a `.env` file in the project root.

Example:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
DATABASE_URL=your_database_url
```

The `.env` file is ignored using `.gitignore` to protect sensitive information.


# Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```


The API will run at:

```
http://127.0.0.1:8000
```


Swagger documentation:

```
http://127.0.0.1:8000/docs
```


# Database

The application uses PostgreSQL with SQLAlchemy.

The application automatically:

- Connects to PostgreSQL
- Creates database tables
- Handles task data persistence


# Authentication

Authentication is handled using **Supabase Auth**.

The authentication flow:

1. User creates an account using signup.
2. User logs in with email and password.
3. Supabase returns a JWT access token.
4. Client sends the token in the Authorization header.
5. Backend verifies the token before allowing access to protected routes.


# API Endpoints

## Authentication

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/auth/signup` | Create a new user account | No |
| POST | `/auth/login` | Login user and receive JWT token | No |
| POST | `/auth/logout` | Logout user session | Yes |


## Protected Routes

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/protected/profile` | Get current user profile | Yes |


## Public Routes

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/public/info` | Get public information | No |


## Task Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/` | Get all tasks |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/{task_id}` | Get task by ID |
| PUT | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |


# Swagger Authentication

To test protected routes:

1. Login using:

```
POST /auth/login
```

2. Copy the returned:

```
access_token
```

3. Click the **Authorize 🔒** button in Swagger UI.

4. Paste the token.

5. Test:

```
GET /protected/profile
```


# Example Protected Response

```json
{
  "message": "Protected profile",
  "user": {
    "id": "user-id",
    "email": "user@email.com"
  }
}
```


# Security

The API uses:

- Supabase JWT authentication
- Bearer token verification
- Environment variables for secrets
- Protected authentication dependencies

Sensitive files are ignored:

```
.env
.venv/
__pycache__/
```


# GitHub

Repository:

https://github.com/MhamzaShahzad535/task-api