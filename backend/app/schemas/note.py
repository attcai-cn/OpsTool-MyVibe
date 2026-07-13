from pydantic import BaseModel, Field
from datetime import datetime


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    tags: str = Field(default="", max_length=200)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class NoteOut(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
