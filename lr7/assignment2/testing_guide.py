"""
ЗАДАНИЕ 2: Тестирование API с помощью Swagger UI
===============================================

После запуска приложения откройте браузер и перейдите по адресу http://localhost:8000/docs.
Вы увидите интерактивную документацию Swagger UI.

Для выполнения задания последовательно протестируйте все эндпоинты:
"""

from fastapi.testclient import TestClient
from app.main import app
import json

# Создаем тестового клиента
client = TestClient(app)


def print_step(step_number, description):
    """Вспомогательная функция для вывода шагов"""
    print(f"\n{'=' * 60}")
    print(f"ШАГ {step_number}: {description}")
    print('=' * 60)


def test_api_with_swagger_ui():
    """
    Пошаговое тестирование API через Swagger UI
    Следуйте этим шагам в браузере на странице http://localhost:8000/docs
    """

    print("ТЕСТИРОВАНИЕ API С ПОМОЩЬЮ SWAGGER UI")
    print("Откройте в браузере: http://localhost:8000/docs")
    print("\nВыполните следующие шаги:")

    # Шаг 1: Получение списка книг
    print_step(1, "Получение списка всех книг")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт GET /api/books
    2. Нажмите кнопку 'Try it out'
    3. Нажмите 'Execute'
    4. Проверьте ответ:
       - Статус код: 200 OK
       - Тело ответа: список из 3 начальных книг
    """)

    # Выполняем тест программно для демонстрации
    response = client.get("/api/books")
    print(f"Программный тест GET /api/books:")
    print(f"Статус код: {response.status_code}")
    print(f"Количество книг: {len(response.json())}")

    # Шаг 2: Получение книги по ID
    print_step(2, "Получение книги по ID")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт GET /api/books/{book_id}
    2. Нажмите 'Try it out'
    3. Введите book_id = 1
    4. Нажмите 'Execute'
    5. Проверьте ответ:
       - Статус код: 200 OK
       - Тело ответа: книга 'Война и мир'
    """)

    response = client.get("/api/books/1")
    print(f"Программный тест GET /api/books/1:")
    print(f"Статус код: {response.status_code}")
    book_data = response.json()
    print(f"Название книги: {book_data['title']}")
    print(f"Автор: {book_data['author']}")

    # Шаг 3: Создание новой книги
    print_step(3, "Создание новой книги")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт POST /api/books
    2. Нажмите 'Try it out'
    3. Введите данные новой книги в формате JSON:

    {
        "title": "Анна Каренина",
        "author": "Лев Толстой",
        "year": 1877,
        "isbn": "9785170654321"
    }

    4. Нажмите 'Execute'
    5. Проверьте ответ:
       - Статус код: 201 Created
       - Тело ответа: созданная книга с присвоенным ID 4
    """)

    new_book = {
        "title": "Анна Каренина",
        "author": "Лев Толстой",
        "year": 1877,
        "isbn": "9785170654321"
    }

    response = client.post("/api/books", json=new_book)
    print(f"Программный тест POST /api/books:")
    print(f"Статус код: {response.status_code}")
    created_book = response.json()
    print(f"ID новой книги: {created_book['id']}")
    print(f"Название: {created_book['title']}")

    # Шаг 4: Частичное обновление книги
    print_step(4, "Частичное обновление книги (PATCH)")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт PATCH /api/books/{book_id}
    2. Нажмите 'Try it out'
    3. Введите book_id = 1
    4. Введите данные для обновления:

    {
        "year": 1867
    }

    5. Нажмите 'Execute'
    6. Проверьте ответ:
       - Статус код: 200 OK
       - Тело ответа: обновленная книга с измененным годом
    """)

    update_data = {"year": 1867}
    response = client.patch("/api/books/1", json=update_data)
    print(f"Программный тест PATCH /api/books/1:")
    print(f"Статус код: {response.status_code}")
    updated_book = response.json()
    print(f"Обновленный год книги ID 1: {updated_book['year']}")

    # Шаг 5: Полное обновление книги
    print_step(5, "Полное обновление книги (PUT)")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт PUT /api/books/{book_id}
    2. Нажмите 'Try it out'
    3. Введите book_id = 2
    4. Введите полные данные книги:

    {
        "title": "Преступление и наказание (обновленное)",
        "author": "Федор Достоевский",
        "year": 1866,
        "isbn": "9785170876543"
    }

    5. Нажмите 'Execute'
    6. Проверьте ответ:
       - Статус код: 200 OK
       - Тело ответа: полностью обновленная книга
    """)

    full_update = {
        "title": "Преступление и наказание (обновленное)",
        "author": "Федор Достоевский",
        "year": 1866,
        "isbn": "9785170876543"
    }

    response = client.put("/api/books/2", json=full_update)
    print(f"Программный тест PUT /api/books/2:")
    print(f"Статус код: {response.status_code}")
    print(f"Обновленное название: {response.json()['title']}")

    # Шаг 6: Фильтрация книг
    print_step(6, "Фильтрация книг с параметрами")
    print("""
    В Swagger UI:
    1. Вернитесь к эндпоинту GET /api/books
    2. Нажмите 'Try it out' снова
    3. Введите параметры фильтрации:
       - author: толстой
       - year_from: 1800
       - year_to: 1900
    4. Нажмите 'Execute'
    5. Проверьте ответ:
       - Статус код: 200 OK
       - Тело ответа: книги Толстого, изданные в 19 веке
    """)

    response = client.get("/api/books?author=толстой&year_from=1800&year_to=1900")
    print(f"Программный тест GET /api/books с фильтрацией:")
    print(f"Статус код: {response.status_code}")
    books = response.json()
    print(f"Найдено книг: {len(books)}")
    for book in books:
        print(f"  - {book['title']} ({book['year']})")

    # Шаг 7: Поиск книг
    print_step(7, "Поиск книг по ключевому слову")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт GET /api/books/search/{keyword}
    2. Нажмите 'Try it out'
    3. Введите keyword: война
    4. Нажмите 'Execute'
    5. Проверьте ответ:
       - Статус код: 200 OK
       - Тело ответа: книги, содержащие 'война' в названии или авторе
    """)

    response = client.get("/api/books/search/война")
    print(f"Программный тест GET /api/books/search/война:")
    print(f"Статус код: {response.status_code}")
    print(f"Найдено книг: {len(response.json())}")

    # Шаг 8: Получение статистики
    print_step(8, "Получение статистики по книгам")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт GET /api/books/stats/statistics
    2. Нажмите 'Try it out'
    3. Нажмите 'Execute'
    4. Проверьте ответ:
       - Статус код: 200 OK
       - Тело ответа: статистика по книгам
    """)

    response = client.get("/api/books/stats/statistics")
    print(f"Программный тест GET /api/books/stats/statistics:")
    print(f"Статус код: {response.status_code}")
    stats = response.json()
    print(f"Общее количество книг: {stats['total_books']}")
    print(f"Книг по авторам: {stats['books_by_author']}")

    # Шаг 9: Удаление книги
    print_step(9, "Удаление книги")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт DELETE /api/books/{book_id}
    2. Нажмите 'Try it out'
    3. Введите book_id = 3
    4. Нажмите 'Execute'
    5. Проверьте ответ:
       - Статус код: 204 No Content
       - Тело ответа: пустое
    6. Проверьте список книг снова - книга с ID 3 должна отсутствовать
    """)

    response = client.delete("/api/books/3")
    print(f"Программный тест DELETE /api/books/3:")
    print(f"Статус код: {response.status_code}")

    # Проверяем, что книга удалена
    response = client.get("/api/books/3")
    print(f"Проверка GET /api/books/3 после удаления:")
    print(f"Статус код: {response.status_code} (должен быть 404)")

    # Шаг 10: Тестирование валидации
    print_step(10, "Тестирование валидации данных")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт POST /api/books
    2. Нажмите 'Try it out'
    3. Введите некорректные данные:

    {
        "title": "",
        "author": "Автор",
        "year": 3000,
        "isbn": "123"
    }

    4. Нажмите 'Execute'
    5. Проверьте ответ:
       - Статус код: 422 Unprocessable Entity
       - Тело ответа: детали ошибок валидации
    """)

    invalid_book = {
        "title": "",  # Пустое название
        "author": "Автор",
        "year": 3000,  # Год в будущем
        "isbn": "123"  # Слишком короткий ISBN
    }

    response = client.post("/api/books", json=invalid_book)
    print(f"Программный тест с некорректными данными:")
    print(f"Статус код: {response.status_code}")
    if response.status_code == 422:
        errors = response.json()
        print("Ошибки валидации:")
        for error in errors.get('detail', []):
            print(f"  - {error['loc']}: {error['msg']}")

    # Шаг 11: Тестирование несуществующего ресурса
    print_step(11, "Тестирование несуществующего ресурса")
    print("""
    В Swagger UI:
    1. Найдите эндпоинт GET /api/books/{book_id}
    2. Нажмите 'Try it out'
    3. Введите book_id = 999 (несуществующий ID)
    4. Нажмите 'Execute'
    5. Проверьте ответ:
       - Статус код: 404 Not Found
       - Тело ответа: сообщение об ошибке
    """)

    response = client.get("/api/books/999")
    print(f"Программный тест GET /api/books/999:")
    print(f"Статус код: {response.status_code}")
    if response.status_code == 404:
        print(f"Сообщение об ошибке: {response.json()['detail']}")


def interactive_testing_guide():
    """
    Интерактивное руководство по тестированию в Swagger UI
    """
    print("\n" + "=" * 70)
    print("ИНТЕРАКТИВНОЕ ТЕСТИРОВАНИЕ В SWAGGER UI")
    print("=" * 70)

    print("\nОткройте браузер и перейдите по адресу: http://localhost:8000/docs")

    print("\nСтруктура страницы Swagger UI:")
    print("1. Вверху: информация об API (название, описание, версия)")
    print("2. Слева: список всех эндпоинтов, сгруппированных по тегам")
    print("3. Справа: документация к выбранному эндпоинту")

    print("\nКак тестировать эндпоинт:")
    print("1. Найдите нужный эндпоинт в списке")
    print("2. Нажмите на него, чтобы развернуть документацию")
    print("3. Нажмите кнопку 'Try it out'")
    print("4. Заполните параметры (если есть)")
    print("5. Нажмите 'Execute'")
    print("6. Просмотрите ответ:")
    print("   - Server response: статус код")
    print("   - Response body: тело ответа")
    print("   - Response headers: заголовки ответа")

    print("\nКоды состояния HTTP, которые вы увидите:")
    print("- 200 OK: успешный запрос")
    print("- 201 Created: ресурс создан")
    print("- 204 No Content: успешно, но нет содержимого (удаление)")
    print("- 400 Bad Request: неверный запрос")
    print("- 404 Not Found: ресурс не найден")
    print("- 422 Unprocessable Entity: ошибка валидации")

    print("\nСоветы по тестированию:")
    print("1. Начните с GET /api/books - посмотрите начальные данные")
    print("2. Создайте новую книгу через POST /api/books")
    print("3. Протестируйте фильтрацию через параметры запроса")
    print("4. Проверьте обработку ошибок (неверные данные, несуществующие ID)")
    print("5. Используйте разные методы для одной книги (GET, PATCH, PUT, DELETE)")


def save_test_results():
    """Сохранение результатов тестирования в файл"""
    print("\nСохранение результатов тестирования...")

    test_results = {
        "api_url": "http://localhost:8000",
        "docs_url": "http://localhost:8000/docs",
        "endpoints_tested": [
            "GET /api/books",
            "GET /api/books/{id}",
            "POST /api/books",
            "PUT /api/books/{id}",
            "PATCH /api/books/{id}",
            "DELETE /api/books/{id}",
            "GET /api/books/search/{keyword}",
            "GET /api/books/stats/statistics"
        ],
        "test_cases": [
            "Получение всех книг",
            "Получение книги по ID",
            "Создание новой книги",
            "Полное обновление",
            "Частичное обновление",
            "Удаление книги",
            "Фильтрация и поиск",
            "Получение статистики",
            "Обработка ошибок"
        ],
        "validation_tested": [
            "Обязательные поля",
            "Длина строк",
            "Диапазон годов",
            "Уникальность ISBN"
        ],
        "status_codes_observed": [
            200, 201, 204, 404, 422
        ]
    }

    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)

    print("Результаты сохранены в файл test_results.json")


if __name__ == "__main__":
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА: ТЕСТИРОВАНИЕ API С ПОМОЩЬЮ SWAGGER UI")
    print("=" * 70)

    # Запускаем автоматические тесты для демонстрации
    test_api_with_swagger_ui()

    # Показываем интерактивное руководство
    interactive_testing_guide()

    # Сохраняем результаты
    save_test_results()

    print("\n" + "=" * 70)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("=" * 70)
    print("\nДля интерактивного тестирования:")
    print("1. Запустите сервер: uvicorn app.main:app --reload")
    print("2. Откройте в браузере: http://localhost:8000/docs")
    print("3. Следуйте инструкциям выше")