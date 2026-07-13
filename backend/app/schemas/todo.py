from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    urgency: Literal["low", "medium", "high"] = "medium"
    deadline: datetime
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class TodoToggle(BaseModel):
    completed: bool


class TodoOut(TodoBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
