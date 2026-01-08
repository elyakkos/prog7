"""
ЧАСТЬ 2: Потоки в Python
Примеры 1.1 - 1.5
"""
import threading
import time
import math
import random
import requests
import os

# 1.1: Создание потоков и вывод имен
def example_1_1():
    print("\n1.1: Создание потоков и вывод имен")

    def print_thread_info(thread_num):
        current = threading.current_thread()
        print(f"Поток {thread_num}: Имя = {current.name}, ID = {current.ident}")
        time.sleep(0.5)

    threads = []
    for i in range(5):
        t = threading.Thread(
            target=print_thread_info,
            args=(i,),
            name=f"Thread-{i}"
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("Все потоки завершены")

# 1.2: Загрузка файлов
def example_1_2():
    print("\n1.2: Загрузка файлов")

    def download_image(url, filename):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Загружен: {filename}")
            else:
                print(f"Ошибка {url}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Ошибка загрузки {url}: {e}")

    # Тестовые URL (замените на реальные для тестирования)
    urls = [
        ("https://picsum.photos/200/300", "image1.jpg"),
        ("https://picsum.photos/200/301", "image2.jpg"),
        ("https://picsum.photos/200/302", "image3.jpg")
    ]

    # Создаем папку для загрузок
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    threads = []
    for url, filename in urls:
        t = threading.Thread(
            target=download_image,
            args=(url, f"downloads/{filename}")
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("Загрузка завершена")

# 1.3: HTTP-запросы
def example_1_3():
    print("\n1.3: HTTP-запросы")

    def make_request(url):
        try:
            response = requests.get(url, timeout=5)
            print(f"{url[:30]}... : Status {response.status_code}")
        except Exception as e:
            print(f"{url[:30]}... : Error - {e}")

    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://httpbin.org/delay/1"
    ]

    threads = []
    for url in urls:
        t = threading.Thread(target=make_request, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("Все запросы выполнены")

# 1.4: Факториал
def example_1_4():
    print("\n1.4: Вычисление факториала")

    def calculate_range(start, end, result_list, idx):
        result = 1
        for i in range(start, end + 1):
            result *= i
        result_list[idx] = result

    def factorial_threaded(n, num_threads=4):
        results = [1] * num_threads
        chunk_size = n // num_threads

        threads = []
        for i in range(num_threads):
            start = i * chunk_size + 1
            end = start + chunk_size - 1 if i < num_threads - 1 else n

            t = threading.Thread(
                target=calculate_range,
                args=(start, end, results, i)
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Умножаем все части
        total = 1
        for r in results:
            total *= r

        return total

    n = 10
    result = factorial_threaded(n, num_threads=2)
    print(f"{n}! = {result}")
    print(f"Проверка (math.factorial): {math.factorial(n)}")

# 1.5: Быстрая сортировка
def example_1_5():
    print("\n1.5: Быстрая сортировка")

    def quick_sort(arr):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return quick_sort(left) + middle + quick_sort(right)

    def quick_sort_threaded(arr, max_depth=2, depth=0):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        if depth < max_depth:
            left_result = []
            right_result = []

            def sort_left():
                nonlocal left_result
                left_result = quick_sort_threaded(left, max_depth, depth + 1)

            def sort_right():
                nonlocal right_result
                right_result = quick_sort_threaded(right, max_depth, depth + 1)

            t1 = threading.Thread(target=sort_left)
            t2 = threading.Thread(target=sort_right)

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            return left_result + middle + right_result
        else:
            return (quick_sort_threaded(left, max_depth, depth + 1) +
                    middle +
                    quick_sort_threaded(right, max_depth, depth + 1))

    # Генерируем тестовый массив
    arr = [random.randint(1, 100) for _ in range(20)]
    print(f"Исходный массив: {arr}")

    # Обычная сортировка
    sorted_arr = quick_sort(arr.copy())
    print(f"Обычная сортировка: {sorted_arr}")

    # Многопоточная сортировка
    threaded_arr = quick_sort_threaded(arr.copy(), max_depth=2)
    print(f"Многопоточная сортировка: {threaded_arr}")

    # Проверка
    print(f"Результаты совпадают: {sorted_arr == threaded_arr}")

def run_all_examples():
    """Запуск всех примеров"""
    print("="*50)
    print("ВСЕ ПРИМЕРЫ С ПОТОКАМИ")
    print("="*50)

    example_1_1()
    # example_1_2()  # Раскомментировать для тестирования загрузки
    example_1_3()
    example_1_4()
    example_1_5()

if __name__ == "__main__":
    run_all_examples()