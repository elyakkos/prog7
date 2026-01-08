"""
ЧАСТЬ 3: Concurrency и Futures
Простые реализации всех заданий 2.1-2.8
"""
import threading
import time
import random
import math
from threading import Lock, RLock, Event, Barrier, Semaphore
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# 2.1: Интегрирование с ThreadPoolExecutor
def example_21():
    print("\n=== 2.1 Интегрирование с concurrent.futures ===")

    def integrate_futures(f, a, b, n_iter=1000000, n_jobs=4):
        dx = (b - a) / n_iter
        chunk = n_iter // n_jobs

        def compute(start):
            s = 0.0
            for i in range(start, start + chunk):
                x = a + i * dx
                s += f(x) * dx
            return s

        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            tasks = []
            for i in range(n_jobs):
                start = i * chunk
                tasks.append(executor.submit(compute, start))

            total = sum(task.result() for task in tasks)

        return total

    result = integrate_futures(math.atan, 0, math.pi / 2, n_iter=1000000, n_jobs=4)
    print(f"Результат: {result}")


# 2.2: Банк с Lock
def example_22():
    print("\n=== 2.2 Банк с Lock ===")

    class Bank:
        def __init__(self, money=1000):
            self.money = money
            self.lock = Lock()

        def deposit(self, amount, name):
            with self.lock:
                old = self.money
                self.money += amount
                print(f"{name}: +{amount}. Было {old}, стало {self.money}")

        def withdraw(self, amount, name):
            with self.lock:
                if self.money >= amount:
                    old = self.money
                    self.money -= amount
                    print(f"{name}: -{amount}. Было {old}, стало {self.money}")
                else:
                    print(f"{name}: Не хватает денег!")

    bank = Bank(2000)

    def client(name, actions):
        for act, amount in actions:
            time.sleep(0.2)
            if act == "д":
                bank.deposit(amount, name)
            else:
                bank.withdraw(amount, name)

    clients = [
        ("Коля", [("д", 100), ("д", 200), ("с", 150)]),
        ("Маша", [("с", 300), ("д", 500), ("с", 100)]),
    ]

    threads = []
    for name, actions in clients:
        t = threading.Thread(target=client, args=(name, actions))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Итог в банке: {bank.money}")


# 2.3: Загрузка с Future и Semaphore
def example_23():
    print("\n=== 2.3 Загрузка с Future и Semaphore ===")

    def download(url, name, sem):
        with sem:
            print(f"Начинаю {name}...")
            time.sleep(random.randint(1, 3))  # Имитация загрузки
            print(f"Загрузил {name}")
            return f"{name} готов"

    urls = ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"]
    semaphore = Semaphore(2)  # Максимум 2 загрузки сразу

    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [executor.submit(download, url, url, semaphore) for url in urls]

        for task in tasks:
            print(task.result())


# 2.4: Чтение/запись файла
def example_24():
    print("\n=== 2.4 Чтение/запись файла ===")

    event = Event()

    def writer():
        with open("test.txt", "w") as f:
            for i in range(3):
                msg = f"Строка {i}\n"
                f.write(msg)
                print(f"Записал: {msg.strip()}")
                event.set()  # Говорим читателю
                time.sleep(1)

    def reader():
        time.sleep(0.5)
        with open("test.txt", "r") as f:
            for i in range(3):
                event.wait()  # Ждем писателя
                line = f.readline()
                print(f"Прочел: {line.strip()}")
                event.clear()

    t1 = threading.Thread(target=writer)
    t2 = threading.Thread(target=reader)

    t1.start()
    t2.start()
    t1.join()
    t2.join()


# 2.5: Event с тремя потоками
def example_25():
    print("\n=== 2.5 Event с тремя потоками ===")

    ev = Event()

    def setter():
        for _ in range(2):
            time.sleep(1)
            print("Устанавливаю событие")
            ev.set()
            time.sleep(0.5)
            ev.clear()

    def waiter():
        print("Жду событие...")
        ev.wait()
        print("Событие случилось!")

    def monitor():
        while not ev.is_set():
            print("События нет")
            time.sleep(1)
        print("Монитор видит событие")

    t1 = threading.Thread(target=setter)
    t2 = threading.Thread(target=waiter)
    t3 = threading.Thread(target=monitor)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


# 2.6: Очередь с RLock
def example_26():
    print("\n=== 2.6 Очередь с RLock ===")

    class MyQueue:
        def __init__(self):
            self.items = []
            self.lock = RLock()

        def put(self, item):
            with self.lock:
                self.items.append(item)
                print(f"Добавил {item}: {self.items}")

        def get(self):
            with self.lock:
                if self.items:
                    item = self.items.pop(0)
                    print(f"Взял {item}: {self.items}")
                    return item
                return None

    q = MyQueue()

    def producer():
        for i in range(3):
            q.put(f"item{i}")
            time.sleep(0.3)

    def consumer():
        for _ in range(3):
            q.get()
            time.sleep(0.5)

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)

    t1.start()
    t2.start()
    t1.join()
    t2.join()


# 2.7: Barrier для клиент-сервера
def example_27():
    print("\n=== 2.7 Barrier для клиент-сервера ===")

    barrier = Barrier(2)

    def server():
        print("Сервер: запускаюсь...")
        time.sleep(2)
        print("Сервер: готов!")
        barrier.wait()
        print("Сервер: получил запрос")

    def client():
        print("Клиент: готовлюсь...")
        time.sleep(1)
        print("Клиент: готов!")
        barrier.wait()
        print("Клиент: отправил запрос")

    t1 = threading.Thread(target=server)
    t2 = threading.Thread(target=client)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


# 2.8: Параллельный поиск файла
def example_28():
    print("\n=== 2.8 Параллельный поиск файла ===")

    found = False
    lock = Lock()

    def search_files(files, pattern, thread_id):
        global found
        for f in files:
            if found:
                return

            if pattern in f:
                with lock:
                    if not found:
                        found = True
                        print(f"Поток {thread_id} нашел: {f}")

    # Имитируем список файлов
    all_files = ["file1.txt", "file2.py", "data.csv", "test.py", "image.jpg", "main.py"]
    pattern = ".py"

    threads = []
    chunk = len(all_files) // 2

    for i in range(2):
        start = i * chunk
        end = start + chunk if i == 0 else len(all_files)
        part = all_files[start:end]

        t = threading.Thread(target=search_files, args=(part, pattern, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not found:
        print(f"Файлы с '{pattern}' не найдены")


def run_all():
    """Запуск всех примеров"""
    print("=" * 50)
    print("CONCURRENCY И FUTURES")
    print("=" * 50)

    example_21()
    example_22()
    example_23()
    example_24()
    example_25()
    example_26()
    example_27()
    example_28()


if __name__ == "__main__":
    run_all()