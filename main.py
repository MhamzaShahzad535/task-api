from fastapi import FastAPI

import models
from database import engine
from routers import auth, tasks, public, protected
from src.routers import ai
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task API",
    version="2.0.0"
)

app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(public.router)
app.include_router(protected.router)
app.include_router(ai.router)


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "2.0.0"
    }