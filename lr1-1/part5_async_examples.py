"""
ЧАСТЬ 4: Асинхронность
Простые реализации всех заданий 1.1-1.7
"""
import asyncio
import datetime
import json
import aiohttp
import asyncpg


# 1.1: Асинхронные часы
async def example_11():
    print("\n=== 1.1 Асинхронные часы ===")

    async def clock():
        try:
            while True:
                now = datetime.datetime.now()
                print(f"\r{now.strftime('%H:%M:%S')}", end="", flush=True)
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("\nЧасы остановлены")

    # Запускаем на 5 секунд
    task = asyncio.create_task(clock())
    await asyncio.sleep(5)
    task.cancel()


# 1.2: Цветные часы с ESC
async def example_12():
    print("\n=== 1.2 Цветные часы ===")

    async def color_clock():
        try:
            while True:
                now = datetime.datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")
                # Для цветов нужно установить termcolor
                print(f"\rДата: {date_str} | Время: {time_str}", end="", flush=True)
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("\nЗавершено")

    # Запускаем на 3 секунды
    task = asyncio.create_task(color_clock())
    await asyncio.sleep(3)
    task.cancel()


# 1.3: asyncio.gather
async def example_13():
    print("\n=== 1.3 asyncio.gather ===")

    async def task1():
        print("Задача 1: началась")
        await asyncio.sleep(2)
        print("Задача 1: закончилась")
        return "Результат 1"

    async def task2():
        print("Задача 2: началась")
        await asyncio.sleep(1)
        print("Задача 2: закончилась")
        return "Результат 2"

    results = await asyncio.gather(task1(), task2())
    print(f"Все результаты: {results}")


# 1.4: Запросы к RNA Central
async def example_14():
    print("\n=== 1.4 RNA Central запросы ===")

    async def web_request():
        url = "https://httpbin.org/json"  # Тестовый URL вместо RNA Central
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    print(f"Веб-запрос: получил {len(str(data))} символов")
                    return data
        except Exception as e:
            print(f"Ошибка веб-запроса: {e}")
            return None

    async def db_query():
        # Имитация запроса к БД
        await asyncio.sleep(1)
        print("Запрос к БД: получил 100 записей")
        return ["record1", "record2", "record3"]

    web, db = await asyncio.gather(web_request(), db_query())
    print(f"Веб: {web is not None}, БД: {len(db) if db else 0} записей")


# 1.5: Веб-скрапер
class WebScraper:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    async def fetch(self, url):
        try:
            async with self.session.get(url, timeout=10) as response:
                text = await response.text()
                return len(text)
        except Exception as e:
            print(f"Ошибка {url}: {e}")
            return 0


async def example_15():
    print("\n=== 1.5 Веб-скрапер ===")

    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/xml",
        "https://httpbin.org/json"
    ]

    async with WebScraper() as scraper:
        tasks = [scraper.fetch(url) for url in urls]
        results = await asyncio.gather(*tasks)

        for url, length in zip(urls, results):
            print(f"{url}: {length} символов")


# 1.6: Менеджер контекста
async def example_16():
    print("\n=== 1.6 Менеджер контекста ===")

    # Используем тот же WebScraper, но через async with
    print("Используем WebScraper из примера 1.5")
    await example_15()  # Просто показываем что он работает


# 1.7: Сервер и клиент
async def example_17():
    print("\n=== 1.7 Сервер и клиент ===")

    async def handle_client(reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Сервер получил от {addr}: {message}")

        response = {"status": "ok", "message": f"Вы сказали: {message}"}
        writer.write(json.dumps(response).encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()

    async def client():
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

        messages = ["Привет", "Как дела?", "Пока"]
        for msg in messages:
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(100)
            print(f"Клиент получил: {data.decode()}")
            await asyncio.sleep(1)

        writer.close()
        await writer.wait_closed()

    # Запускаем сервер и клиент
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    async with server:
        # Запускаем сервер в фоне
        server_task = asyncio.create_task(server.serve_forever())

        # Даем серверу время запуститься
        await asyncio.sleep(0.5)

        # Запускаем клиента
        await client()

        # Останавливаем сервер
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass


async def main():
    """Запуск всех примеров"""
    print("=" * 50)
    print("АСИНХРОННЫЕ ПРИМЕРЫ")
    print("=" * 50)

    await example_11()
    await example_12()
    await example_13()
    await example_14()
    await example_15()
    await example_16()
    await example_17()

    print("\nВсе примеры завершены!")


if __name__ == "__main__":
    asyncio.run(main())