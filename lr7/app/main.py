from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Импорт CORS
from app.api.books import router as books_router
from app.database import engine, Base

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Создание экземпляра приложения FastAPI
app = FastAPI(
    title="Books API",
    description="REST API для управления библиотекой книг",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники (для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Корневой эндпоинт
@app.get("/", tags=["Root"])
async def root():
    """
    Корневой эндпоинт API.
    Возвращает приветственное сообщение и ссылки на документацию.
    """
    return {
        "message": "Добро пожаловать в Books API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }

# Подключение роутера книг
app.include_router(books_router, prefix="/api")

# Точка входа для запуска приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)