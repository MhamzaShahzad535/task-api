from pydantic import BaseModel


class TaskCreate(BaseModel):

    title: str



class TaskResponse(BaseModel):

    id: int
    title: str
    done: bool


    class Config:
        from_attributes = True