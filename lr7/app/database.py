from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Создание движка базы данных SQLite
DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


# Модель таблицы Book для SQLAlchemy
class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    isbn = Column(String(13), nullable=True)
    created_at = Column(DateTime, default=func.now())


# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создание начальных данных
def init_db():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже книги в базе
        if db.query(BookDB).count() == 0:
            # Добавляем начальные данные
            initial_books = [
                BookDB(
                    title="Война и мир",
                    author="Лев Толстой",
                    year=1869,
                    isbn="9785170987654"
                ),
                BookDB(
                    title="Преступление и наказание",
                    author="Федор Достоевский",
                    year=1866,
                    isbn="9785170876543"
                ),
                BookDB(
                    title="Евгений Онегин",
                    author="Александр Пушкин",
                    year=1833,
                    isbn="9785170765432"
                )
            ]
            db.add_all(initial_books)
            db.commit()
            print("База данных инициализирована с начальными данными")
    except Exception as e:
        print(f"Ошибка инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()


# Инициализируем базу данных при импорте
init_db()