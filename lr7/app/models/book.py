from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


# Модель данных для книги (Pydantic схема)
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название книги")
    author: str = Field(..., min_length=1, max_length=100, description="Автор книги")
    year: int = Field(..., ge=1000, le=datetime.now().year, description="Год издания")
    isbn: Optional[str] = Field(None, min_length=10, max_length=13, description="ISBN книги")


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)


class Book(BookBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Для SQLAlchemy моделей
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Мастер и Маргарита",
                "author": "Михаил Булгаков",
                "year": 1967,
                "isbn": "9785170123456",
                "created_at": "2023-11-15T10:30:00"
            }
        }


# Модель для статистики
class StatisticsResponse(BaseModel):
    total_books: int
    books_by_author: dict
    books_by_century: dict