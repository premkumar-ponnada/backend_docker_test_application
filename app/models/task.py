"""Pydantic models = the shape of the data going in and out of the API."""

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """What the client sends when creating a task (POST /tasks)."""

    title: str = Field(..., min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title must not be empty or whitespace only")
        return cleaned


class Task(BaseModel):
    """What the API sends back. Each task is just an id + a title."""

    id: int
    title: str
