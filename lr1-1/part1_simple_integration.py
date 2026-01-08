"""
ЧАСТЬ 1: Простое интегрирование
Последовательное вычисление интеграла
"""
import math
import timeit

def integrate(f, a, b, *, n_iter=1000):
    """Написание программы для численного интегрирования площади под кривой."""
    dx = (b - a) / n_iter
    total = 0.0
    for i in range(n_iter):
        x = a + i * dx
        total += f(x) * dx
    return total

def integrate2(f, a, b, n_iter=1000):
    """Альтернативная версия"""
    dx = (b - a) / n_iter
    total = 0.0
    for i in range(n_iter):
        x = a + i * dx
        total += f(x) * dx
    return total

def test_performance():
    """Тестирование производительности"""
    print("="*50)
    print("ТЕСТИРОВАНИЕ ПОСЛЕДОВАТЕЛЬНОГО ИНТЕГРИРОВАНИЯ")
    print("="*50)

    # Тест 1: n_iter = 10^4
    t1 = timeit.timeit(
        'integrate(math.sin, 0, 1, n_iter=10000)',
        setup='from __main__ import integrate, math',
        number=10
    )
    print(f"n_iter = 10^4: {t1:.4f} сек")

    # Тест 2: n_iter = 10^5
    t2 = timeit.timeit(
        'integrate(math.sin, 0, 1, n_iter=100000)',
        setup='from __main__ import integrate, math',
        number=10
    )
    print(f"n_iter = 10^5: {t2:.4f} сек")

    # Тест 3: n_iter = 10^6
    t3 = timeit.timeit(
        'integrate(math.sin, 0, 1, n_iter=1000000)',
        setup='from __main__ import integrate, math',
        number=10
    )
    print(f"n_iter = 10^6: {t3:.4f} сек")

    # Проверка точности
    result = integrate(math.sin, 0, math.pi/2, n_iter=1000000)
    print(f"\n∫sin(x)dx от 0 до π/2 ≈ {result:.8f}")
    print(f"Точное значение: {1 - math.cos(math.pi/2):.8f}")

if __name__ == "__main__":
    test_performance()