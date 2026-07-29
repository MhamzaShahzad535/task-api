from fastapi import FastAPI

from database import Base, engine
from routers import tasks



Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Task API",
    version="4.0.0"
)



app.include_router(
    tasks.router
)



@app.get("/")
def root():

    return {
        "name": "Task API",
        "version": "4.0.0",
        "database": "PostgreSQL + SQLAlchemy"
    }