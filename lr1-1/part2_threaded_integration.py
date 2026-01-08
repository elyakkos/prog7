"""
ЧАСТЬ 2: Многопоточное интегрирование
Использование Thread и Lock
"""
import threading
import math
import time


def integrate_threaded(f, a, b, n_iter=1000, n_threads=4):
    """
    Многопоточное интегрирование с использованием Lock
    """
    dx = (b - a) / n_iter
    total = 0.0
    lock = threading.Lock()

    def worker(start_idx, end_idx):
        nonlocal total
        partial_sum = 0.0
        for i in range(start_idx, end_idx):
            x = a + i * dx
            partial_sum += f(x) * dx

        # Синхронизированный доступ к общей сумме
        with lock:
            total += partial_sum

    # Создание и запуск потоков
    threads = []
    chunk_size = n_iter // n_threads

    for i in range(n_threads):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < n_threads - 1 else n_iter

        thread = threading.Thread(
            target=worker,
            args=(start_idx, end_idx),
            name=f"Worker-{i}"
        )
        threads.append(thread)
        thread.start()

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    return total


def compare_performance():
    """Сравнение последовательного и многопоточного подхода"""
    print("=" * 50)
    print("СРАВНЕНИЕ ПОСЛЕДОВАТЕЛЬНОГО И МНОГОПОТОЧНОГО РЕШЕНИЯ")
    print("=" * 50)

    from part1_simple_integration import integrate

    n_iter = 1000000
    print(f"\nТестирование для n_iter = {n_iter}")

    # Последовательное выполнение
    start = time.time()
    result_seq = integrate(math.sin, 0, 1, n_iter=n_iter)
    time_seq = time.time() - start
    print(f"Последовательное: {time_seq:.4f} сек, результат: {result_seq:.8f}")

    # Многопоточное выполнение (4 потока)
    start = time.time()
    result_thread = integrate_threaded(math.sin, 0, 1, n_iter=n_iter, n_threads=4)
    time_thread = time.time() - start
    print(f"Многопоточное (4 потока): {time_thread:.4f} сек, результат: {result_thread:.8f}")

    # Сравнение
    speedup = time_seq / time_thread
    diff = abs(result_seq - result_thread)
    print(f"\nУскорение: {speedup:.2f}x")
    print(f"Разница результатов: {diff:.10f}")
    print(f"Разница в процентах: {diff / result_seq * 100:.6f}%")


if __name__ == "__main__":
    compare_performance()