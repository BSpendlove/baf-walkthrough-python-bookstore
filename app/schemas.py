from datetime import datetime

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    price: float = Field(gt=0)
    published_year: int | None = Field(default=None, ge=1000, le=2100)
    description: str | None = None


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    price: float | None = Field(default=None, gt=0)
    published_year: int | None = Field(default=None, ge=1000, le=2100)
    description: str | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    price: float
    published_year: int | None
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
