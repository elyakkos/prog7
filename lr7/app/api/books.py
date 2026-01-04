from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from collections import Counter

from app.database import get_db, BookDB
from app.models.book import Book, BookCreate, BookUpdate, StatisticsResponse

router = APIRouter(prefix="/books", tags=["Books"])


# GET /api/books - Получение списка всех книг
@router.get("/", response_model=List[Book])
async def get_books(
        skip: int = Query(default=0, description="Количество книг для пропуска (по умолчанию 0)"),
        limit: int = Query(default=100, description="Максимальное количество книг в ответе (по умолчанию 100)"),
        author: Optional[str] = Query(default=None, description="Фильтр по автору (частичное совпадение)"),
        year_from: Optional[int] = Query(default=None, description="Минимальный год издания"),
        year_to: Optional[int] = Query(default=None, description="Максимальный год издания"),
        db: Session = Depends(get_db)
):
    """
    Получить список книг с возможностью фильтрации и пагинации.

    Параметры:
    - **skip**: Количество книг для пропуска (по умолчанию 0)
    - **limit**: Максимальное количество книг в ответе (по умолчанию 100)
    - **author**: Фильтр по автору (частичное совпадение)
    - **year_from**: Минимальный год издания
    - **year_to**: Максимальный год издания

    Возвращает список книг согласно указанным параметрам.
    """
    query = db.query(BookDB)

    if author:
        query = query.filter(BookDB.author.ilike(f"%{author}%"))
    if year_from:
        query = query.filter(BookDB.year >= year_from)
    if year_to:
        query = query.filter(BookDB.year <= year_to)

    books = query.offset(skip).limit(limit).all()
    return books


# Остальные функции остаются без изменений...

# GET /api/books/{book_id} - Получение книги по ID
@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Получить книгу по ID.

    Параметры:
    - **book_id**: ID книги (целое число)

    Возвращает информацию о книге с указанным ID.
    Если книга не найдена, возвращается ошибка 404.
    """
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    return book


# POST /api/books - Создание новой книги
@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Создать новую книгу.

    Принимает данные новой книги и добавляет её в базу данных.
    Автоматически генерирует уникальный ID для книги.
    Возвращает созданную книгу с присвоенным ID.
    """
    # Проверяем, существует ли книга с таким ISBN
    if book.isbn:
        existing_book = db.query(BookDB).filter(BookDB.isbn == book.isbn).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Книга с ISBN {book.isbn} уже существует"
            )

    db_book = BookDB(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# PUT /api/books/{book_id} - Полное обновление книги
@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    """
    Полностью обновить информацию о книге.

    Параметры:
    - **book_id**: ID книги для обновления
    - **updated_book**: Новые данные книги (все поля обязательны)

    Заменяет все данные книги новыми значениями.
    Если книга не найдена, возвращается ошибка 404.
    """
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )

    # Проверяем ISBN, если он изменен
    if updated_book.isbn and updated_book.isbn != db_book.isbn:
        existing_book = db.query(BookDB).filter(
            BookDB.isbn == updated_book.isbn,
            BookDB.id != book_id
        ).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Книга с ISBN {updated_book.isbn} уже существует"
            )

    # Обновляем все поля
    for field, value in updated_book.model_dump().items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


# PATCH /api/books/{book_id} - Частичное обновление книги
@router.patch("/{book_id}", response_model=Book)
async def partial_update_book(
        book_id: int,
        book_update: BookUpdate,
        db: Session = Depends(get_db)
):
    """
    Частично обновить информацию о книге.

    Параметры:
    - **book_id**: ID книги для обновления
    - **book_update**: Данные для обновления (только указанные поля будут изменены)

    Обновляет только те поля, которые были переданы в запросе.
    Если книга не найдена, возвращается ошибка 404.
    """
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )

    # Получаем только переданные поля (исключаем None)
    update_data = book_update.model_dump(exclude_unset=True)

    # Проверяем ISBN, если он изменен
    if 'isbn' in update_data and update_data['isbn'] != db_book.isbn:
        existing_book = db.query(BookDB).filter(
            BookDB.isbn == update_data['isbn'],
            BookDB.id != book_id
        ).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Книга с ISBN {update_data['isbn']} уже существует"
            )

    # Обновляем только переданные поля
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


# DELETE /api/books/{book_id} - Удаление книги
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Удалить книгу по ID.

    Параметры:
    - **book_id**: ID книги для удаления

    Удаляет книгу из системы.
    Если книга не найдена, возвращается ошибка 404.
    """
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )

    db.delete(db_book)
    db.commit()
    return


# GET /api/books/stats - Статистика по книгам
# GET /api/books/stats/statistics - Статистика по книгам
@router.get("/stats/statistics", response_model=StatisticsResponse, tags=["Statistics"])
async def get_statistics(db: Session = Depends(get_db)):
    """
    Получить статистику по книгам.

    Возвращает:
    - Общее количество книг
    - Распределение по авторам
    - Распределение по векам
    """
    books = db.query(BookDB).all()

    if not books:
        return {
            "total_books": 0,
            "books_by_author": {},
            "books_by_century": {}
        }

    total_books = len(books)
    authors = Counter(book.author for book in books)
    centuries = Counter(book.year // 100 + 1 for book in books)

    return {
        "total_books": total_books,
        "books_by_author": dict(authors),
        "books_by_century": {f"{century} век": count for century, count in centuries.items()}
    }


# GET /api/books/search/{keyword} - Поиск книг
@router.get("/search/{keyword}", response_model=List[Book])
async def search_books(keyword: str, db: Session = Depends(get_db)):
    """
    Поиск книг по ключевому слову.

    Параметры:
    - **keyword**: Ключевое слово для поиска

    Ищет ключевое слово в названии и авторе книги.
    Возвращает список найденных книг.
    """
    books = db.query(BookDB).filter(
        (BookDB.title.ilike(f"%{keyword}%")) |
        (BookDB.author.ilike(f"%{keyword}%"))
    ).all()

    return books