
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# 1. РЕШЕНИЕ ЗАДАЧИ
print("="*60)
print("ЗАДАЧА 1: ОПТИМИЗАЦИЯ ПРОИЗВОДСТВА ЭЛЕКТРОНИКИ")
print("="*60)

# Целевая функция (для максимизации прибыли нужно минимизировать -P)
c = [-8000, -12000]

# Ограничения-неравенства A_ub @ x <= b_ub
A_ub = [
    [2, 3],
    [4, 6],
    [1, 2]
]
b_ub = [240, 480, 150]

# Границы переменных
bounds = [(0, None), (0, None)]

# Решение задачи
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

# Вывод результатов
print("=== Задача оптимизации производства электроники ===")
print(f"Статус: {result.message}")
print(f"Оптимальное количество смартфонов (x₁): {result.x[0]:.0f} шт.")
print(f"Оптимальное количество планшетов (x₂): {result.x[1]:.0f} шт.")
print(f"Максимальная прибыль: {-result.fun:,.0f} руб.")

# 2. ВИЗУАЛИЗАЦИЯ
fig, ax = plt.subplots(figsize=(10, 8))

# Диапазон значений
x1 = np.linspace(0, 150, 400)

# Границы ограничений (выразите x_2 через x_1)
x2_constraint1 = (240 - 2*x1) / 3
x2_constraint2 = (480 - 4*x1) / 6
x2_constraint3 = (150 - x1) / 2

# Построение прямых ограничений
ax.plot(x1, x2_constraint1, 'b-', label='Процессорное время: $2x_1 + 3x_2 \leq 240$')
ax.plot(x1, x2_constraint2, 'g-', label='Оперативная память: $4x_1 + 6x_2 \leq 480$')
ax.plot(x1, x2_constraint3, 'r-', label='Аккумуляторы: $x_1 + 2x_2 \leq 150$')
ax.axhline(0, color='gray', linestyle='--', label='$x_2 \geq 0$')
ax.axvline(0, color='gray', linestyle='--', label='$x_1 \geq 0$')

vertices = [
    (0, 0),
    (120, 0),
    (90, 20),  # Решение системы: 2x1+3x2=240 и x1+2x2=150
    (0, 75)
]

from matplotlib.patches import Polygon
polygon = Polygon(vertices, alpha=0.3, color='lightblue', label='Допустимая область')
ax.add_patch(polygon)

ax.plot(result.x[0], result.x[1], 'ro', markersize=10,
        label=f'Оптимум: ({result.x[0]:.0f}, {result.x[1]:.0f})')

# Линии уровня (изопрофиты) для прибыли
for profit in [400000, 800000, 1200000]:
    x2_profit = (profit - 8000*x1) / 12000
    ax.plot(x1, x2_profit, 'y--', alpha=0.5, linewidth=0.8)

# Линия уровня через оптимум
profit_opt = 8000*result.x[0] + 12000*result.x[1]
x2_opt_line = (profit_opt - 8000*x1) / 12000
ax.plot(x1, x2_opt_line, 'y-', linewidth=2, alpha=0.7,
        label=f'Изопрофита: {profit_opt:,.0f} руб.')

ax.set_xlabel('$x_1$ (смартфоны)', fontsize=12)
ax.set_ylabel('$x_2$ (планшеты)', fontsize=12)
ax.set_title('Задача оптимизации производства: Геометрическое представление', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('task1_exact.png', dpi=300)
plt.show()

print(f"\nГрафик сохранён в: task1_exact.png")