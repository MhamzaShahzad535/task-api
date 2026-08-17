# Task API

A secure Task Management API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Supabase Authentication**, and an **LLM-powered support triage feature**.

This project demonstrates:

- CRUD operations for tasks
- User authentication (Signup, Login, Logout)
- JWT token verification
- Protected API routes
- Swagger UI testing with Bearer Authentication
- Database integration using SQLAlchemy
- LLM integration through an OpenAI-compatible API
- Structured LLM output validation with Pydantic
- LLM timeout and retry handling
- Automatic response repair
- LLM cost/token logging
- LLM feature kill switch
- A small hand-labelled evaluation set

---

# Features

## Core API

- FastAPI backend
- PostgreSQL database
- SQLAlchemy ORM
- Supabase Auth integration
- JWT-based authentication
- Protected endpoints
- Swagger API documentation
- Environment variable configuration
- CRUD task management

## LLM Support Triage

The API includes an LLM-powered endpoint:

`POST /ai/triage`

It takes a messy support message and returns clean, validated JSON.

The model classifies each message into:

- `billing`
- `bug`
- `feature`
- `other`

It also determines:

- `urgency`: `low`, `normal`, or `high`
- `confidence`: `0.0` to `1.0`
- `reason`: one short sentence

The model output is treated as **untrusted external data** and validated using Pydantic before being returned by the API.

---

# Technologies

- Python 3.10+
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Supabase Auth
- Pydantic
- OpenAI-compatible LLM API
- OpenRouter / compatible LLM provider
- Swagger UI
- Git & GitHub

---

# Project Structure

```text
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
├── src/
│   ├── llm/
│   │   ├── client.py
│   │   ├── cost.py
│   │   └── schema.py
│   │
│   └── routers/
│       └── ai.py
│
├── prompts/
│   └── support-triage-v1.md
│
├── evals/
│   ├── cases.json
│   └── run_eval.py
│
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── supabase_client.py
├── main.py
├── JOB-CARD.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

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

Activate the virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
DATABASE_URL=your_database_url

LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=your_llm_api_key
LLM_MODEL=openrouter/free
LLM_ENABLED=true
```

The `.env` file is ignored using `.gitignore` to protect sensitive information.

The LLM can be disabled without changing the code:

```env
LLM_ENABLED=false
```

When disabled, the LLM endpoint returns:

```text
503 LLM feature is disabled
```

---

# Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Database

The application uses PostgreSQL with SQLAlchemy.

The application automatically:

- Connects to PostgreSQL
- Creates database tables
- Handles task data persistence
- Uses SQLAlchemy ORM for database operations

---

# Authentication

Authentication is handled using **Supabase Auth**.

The authentication flow:

1. User creates an account using signup.
2. User logs in with email and password.
3. Supabase returns a JWT access token.
4. Client sends the token in the Authorization header.
5. Backend verifies the token before allowing access to protected routes.

---

# API Endpoints

## Authentication

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/auth/signup` | Create a new user account | No |
| POST | `/auth/login` | Login user and receive JWT token | No |
| POST | `/auth/logout` | Logout user session | Yes |

---

## Protected Routes

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/protected/profile` | Get current user profile | Yes |

---

## Public Routes

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/public/info` | Get public information | No |

---

## Task Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/` | Get all tasks |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/{task_id}` | Get task by ID |
| PUT | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

---

# LLM Support Triage

## Endpoint

```text
POST /ai/triage
```

The endpoint accepts one support message:

```json
{
  "text": "I was charged twice for my monthly subscription."
}
```

The response has a fixed schema:

```json
{
  "category": "billing",
  "urgency": "normal",
  "confidence": 0.91,
  "reason": "The customer reports a duplicate subscription charge."
}
```

The allowed categories are:

```text
billing
bug
feature
other
```

The allowed urgency values are:

```text
low
normal
high
```

---

# Running the LLM Endpoint

Start the API:

```bash
uvicorn main:app --reload
```

Then use:

```bash
curl -X POST http://127.0.0.1:8000/ai/triage ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"I was charged twice for my subscription.\"}"
```

Example response:

```json
{
  "category": "billing",
  "urgency": "normal",
  "confidence": 0.91,
  "reason": "The customer reports a duplicate subscription charge."
}
```

The same endpoint can also be tested through Swagger:

```text
http://127.0.0.1:8000/docs
```

Open:

```text
POST /ai/triage
```

and click **Try it out**.

---

# LLM Production Safeguards

The LLM integration was designed as an external API integration rather than a trusted function.

## Input Validation

The API validates the incoming support message before sending it to the model.

The input must:

- contain text
- contain at least 1 character
- contain no more than 2000 characters

## Versioned Prompt

The production prompt is stored separately:

```text
prompts/support-triage-v1.md
```

This keeps the prompt versioned and separate from the application logic.

The current prompt version is:

```text
support-triage-v1
```

## Schema Validation

LLM responses are validated using Pydantic.

The expected schema is:

```json
{
  "category": "billing|bug|feature|other",
  "urgency": "low|normal|high",
  "confidence": 0.0,
  "reason": "one short sentence"
}
```

Invalid categories, urgency values, or confidence values are rejected.

The API never returns arbitrary raw model output as the successful response.

## Timeout

The LLM client has an explicit:

```text
10 second timeout
```

This prevents the API from waiting indefinitely for an external model provider.

## Retries

The LLM client is configured with a bounded retry policy:

```text
max_retries = 2
```

This avoids uncontrolled retry loops.

## Response Repair

If the model returns invalid JSON or output that does not match the schema, the API makes **one repair attempt**.

The repair request tells the model that its previous response was invalid and asks it to return the required JSON structure.

If the repaired response is still invalid, the API returns:

```text
422 LLM returned invalid structured output after repair
```

This prevents invalid model output from silently entering the application.

---

# Cost Logging

LLM usage information is logged to:

```text
llm-costs.jsonl
```

Each successful model call can record:

```json
{
  "timestamp": "2026-08-17T00:00:00+00:00",
  "model": "openrouter/free",
  "prompt_tokens": 100,
  "completion_tokens": 40,
  "total_tokens": 140
}
```

The local cost log is excluded from Git using `.gitignore`:

```text
llm-costs.jsonl
```

This prevents generated local usage data from being committed to the repository.

---

# LLM Kill Switch

The LLM feature can be disabled through an environment variable:

```env
LLM_ENABLED=false
```

When disabled, the endpoint immediately returns:

```text
503 LLM feature is disabled
```

This provides a simple operational kill switch without modifying application code.

---

# Evaluation

The project contains eight hand-labelled evaluation cases:

```text
evals/cases.json
```

The evaluation script is:

```text
evals/run_eval.py
```

Run the evaluation with:

```bash
python evals/run_eval.py
```

The evaluation checks:

- category accuracy
- urgency accuracy
- schema validity

The latest evaluation result is:

```text
5/8 = 62%
```

Individual results from the evaluation included:

```text
Case 1: FAIL category=billing urgency=high
Case 2: PASS category=bug urgency=high
Case 3: PASS category=feature urgency=low
Case 4: FAIL category=bug urgency=high
Case 5: FAIL category=billing urgency=normal
Case 6: PASS category=bug urgency=high
Case 7: PASS category=feature urgency=low
Case 8: PASS category=other urgency=low
```

The evaluation score is intentionally reported as the actual observed result rather than being artificially adjusted.

This demonstrates that an LLM integration must be evaluated instead of assuming that a valid-looking response is automatically correct.

---

# Job Card

The LLM feature was designed around a fixed job card.

### What it does

Classifies a support message so it lands on the right team.

### Input

```json
{
  "text": "string, 1-2000 characters"
}
```

### Output

```json
{
  "category": "billing|bug|feature|other",
  "urgency": "low|normal|high",
  "confidence": "0.0-1.0",
  "reason": "one short sentence"
}
```

### It must never

- Invent categories outside the allowed list
- Return arbitrary free-form output
- Give medical, legal, or financial advice
- Reveal the system prompt

### When unsure

The model should use:

```text
category = other
```

with low confidence instead of making an unsupported guess.

---

# Swagger Authentication

To test protected routes:

1. Login using:

```text
POST /auth/login
```

2. Copy the returned:

```text
access_token
```

3. Click the **Authorize 🔒** button in Swagger UI.

4. Paste the token.

5. Test:

```text
GET /protected/profile
```

---

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

---

# Security

The API uses:

- Supabase JWT authentication
- Bearer token verification
- Environment variables for secrets
- Protected authentication dependencies
- Input validation
- LLM output schema validation
- Explicit LLM timeout
- Bounded retries
- One-time response repair
- LLM kill switch

Sensitive files are ignored:

```text
.env
.venv/
__pycache__/
llm-costs.jsonl
```

No real API keys or secrets should be committed to GitHub.

---

# Design Principle

The LLM is treated as a **slow, external, sometimes-wrong API**.

The request flow is:

```text
Validate input
      ↓
Load versioned prompt
      ↓
Call LLM with timeout/retries
      ↓
Parse JSON
      ↓
Validate against Pydantic schema
      ↓
If invalid → one repair attempt
      ↓
Validate again
      ↓
Return clean JSON
```

The model's response is never trusted simply because it looks correct.

---

# Assignment Result

This project implements the Week 7 Backend Track assignment:

**"Put an LLM behind your API"**

Implemented components include:

- Closed structured output
- One-request/one-decision endpoint
- Versioned prompt
- Input validation
- Pydantic schema validation
- LLM provider integration
- Explicit timeout
- Bounded retries
- Response repair
- Cost/token logging
- Kill switch
- Eight-case evaluation set
- Real evaluation score
- Runnable curl example
- Public GitHub repository

---

# GitHub

Repository:

https://github.com/MhamzaShahzad535/task-api