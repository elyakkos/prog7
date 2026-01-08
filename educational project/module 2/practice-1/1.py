"""
Практическая работа 1: Обработка журнала успеваемости
Упрощенная версия, соответствующая заданию
"""

import pandas as pd
import numpy as np
from datetime import datetime


# ============================================
# ЗАГРУЗКА ДАННЫХ
# ============================================

def load_journal(filename='journal.csv'):
    """Загрузка журнала из файла"""
    try:
        df = pd.read_csv(filename, encoding='utf-8')
        print(f"✅ Данные успешно загружены из {filename}")
        print(f"   Количество учеников: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден!")
        print("   Создайте файл journal.csv со следующими данными:")
        print("""Ученик,Математика,Русский,Физика,Информатика,История
Иванов И.И.,5,4,5,5,4
Петрова М.А.,4,5,4,5,4
Сидоров П.С.,3,4,3,4,3
Козлова А.В.,5,5,5,5,5
Смирнов Д.И.,4,3,4,5,3
Новикова Е.П.,5,5,4,5,5
Фёдоров А.Н.,3,3,3,3,3
Морозова К.С.,4,4,4,4,4
Соколов В.П.,5,4,5,4,5
Лебедева О.М.,3,4,3,4,4""")
        return None


# ============================================
# АНАЛИЗ ДАННЫХ
# ============================================

def calculate_statistics(df):
    """Расчёт статистики по журналу"""

    # Определяем столбцы с предметами (все кроме первого)
    subject_columns = df.columns[1:]

    # 1. Расчёт среднего балла каждого ученика
    df['Средний_балл'] = df[subject_columns].mean(axis=1).round(2)

    # 2. Определение статуса ученика
    def get_status(avg):
        if avg >= 4.5:
            return 'Отличник'
        elif avg >= 3.5:
            return 'Хорошист'
        elif avg >= 2.5:
            return 'Троечник'
        else:
            return 'Требует внимания'

    df['Статус'] = df['Средний_балл'].apply(get_status)

    return df, subject_columns


# ============================================
# ФУНКЦИИ ДЛЯ АНАЛИЗА
# ============================================

def get_top_students(df, n=5):
    """Топ-N лучших учеников"""
    return df.nlargest(n, 'Средний_балл')[['Ученик', 'Средний_балл', 'Статус']]


def get_struggling_students(df, threshold=3.5):
    """Ученики, требующие внимания (средний балл < 3.5)"""
    return df[df['Средний_балл'] < threshold][['Ученик', 'Средний_балл', 'Статус']]


def get_subject_statistics(df, subject_columns):
    """Статистика по каждому предмету"""
    stats = {}
    for subject in subject_columns:
        stats[subject] = {
            'Средний': df[subject].mean(),
            'Мин': df[subject].min(),
            'Макс': df[subject].max(),
            'Медиана': df[subject].median()
        }
    return stats


def get_class_statistics(df):
    """Общая статистика по классу"""
    stats = {
        'Всего учеников': len(df),
        'Средний балл класса': df['Средний_балл'].mean(),
        'Мин балл': df['Средний_балл'].min(),
        'Макс балл': df['Средний_балл'].max(),
        'Медиана': df['Средний_балл'].median()
    }

    # Количество по статусам
    for status in ['Отличник', 'Хорошист', 'Троечник', 'Требует внимания']:
        count = len(df[df['Статус'] == status])
        stats[f'{status}'] = count

    return stats


# ============================================
# СОХРАНЕНИЕ РЕЗУЛЬТАТОВ
# ============================================

def save_to_excel(df, filename='journal_analysis.xlsx'):
    """Сохранение результатов в Excel"""
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Лист 1: Все данные с сортировкой
            df_sorted = df.sort_values('Средний_балл', ascending=False)
            df_sorted.to_excel(writer, sheet_name='Все ученики', index=False)

            # Лист 2: Отличники и хорошисты
            good_students = df[df['Статус'].isin(['Отличник', 'Хорошист'])]
            good_students.to_excel(writer, sheet_name='Успевающие', index=False)

            # Лист 3: Требующие внимания
            struggling = df[df['Статус'] == 'Требует внимания']
            if len(struggling) > 0:
                struggling.to_excel(writer, sheet_name='Требуют внимания', index=False)

        print(f"✅ Результаты сохранены в {filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении в Excel: {e}")
        return False


def create_text_report(df, class_stats, subject_stats, filename='report.txt'):
    """Создание текстового отчёта"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("ОТЧЁТ ПО УСПЕВАЕМОСТИ КЛАССА\n")
            f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y')}\n")
            f.write("=" * 60 + "\n\n")

            # Общая статистика
            f.write("ОБЩАЯ СТАТИСТИКА:\n")
            f.write("-" * 60 + "\n")
            for key, value in class_stats.items():
                if isinstance(value, float):
                    f.write(f"{key}: {value:.2f}\n")
                else:
                    f.write(f"{key}: {value}\n")

            # Статистика по предметам
            f.write("\nСТАТИСТИКА ПО ПРЕДМЕТАМ:\n")
            f.write("-" * 60 + "\n")
            for subject, stats in subject_stats.items():
                f.write(f"\n{subject}:\n")
                f.write(f"  Средний балл: {stats['Средний']:.2f}\n")
                f.write(f"  Мин: {stats['Мин']}, Макс: {stats['Макс']}\n")

            # Топ-5 учеников
            f.write("\nТОП-5 ЛУЧШИХ УЧЕНИКОВ:\n")
            f.write("-" * 60 + "\n")
            top = get_top_students(df, 5)
            for i, (_, row) in enumerate(top.iterrows(), 1):
                f.write(f"{i}. {row['Ученик']}: {row['Средний_балл']:.2f} ({row['Статус']})\n")

            # Ученики, требующие внимания
            struggling = get_struggling_students(df)
            if len(struggling) > 0:
                f.write("\nУЧЕНИКИ, ТРЕБУЮЩИЕ ВНИМАНИЯ:\n")
                f.write("-" * 60 + "\n")
                for _, row in struggling.iterrows():
                    f.write(f"• {row['Ученик']}: {row['Средний_балл']:.2f}\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write("Конец отчёта\n")
            f.write("=" * 60 + "\n")

        print(f"✅ Текстовый отчёт сохранён в {filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании отчёта: {e}")
        return False


# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================

def main():
    """Основная функция программы"""

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЖУРНАЛА УСПЕВАЕМОСТИ")
    print("=" * 60)

    # 1. Загрузка данных
    df = load_journal('journal.csv')
    if df is None:
        return

    # Показать первые 5 строк
    print("\nПервые 5 записей журнала:")
    print(df.head())

    # 2. Расчёт статистики
    print("\n" + "-" * 60)
    print("РАСЧЁТ СТАТИСТИКИ...")
    df, subjects = calculate_statistics(df)

    # 3. Получение статистики
    class_stats = get_class_statistics(df)
    subject_stats = get_subject_statistics(df, subjects)

    # 4. Вывод результатов в консоль
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА:")
    print("=" * 60)

    print(f"\n📊 ОБЩАЯ СТАТИСТИКА КЛАССА:")
    print(f"   Всего учеников: {class_stats['Всего учеников']}")
    print(f"   Средний балл класса: {class_stats['Средний балл класса']:.2f}")
    print(f"   Мин балл: {class_stats['Мин балл']:.2f}, Макс балл: {class_stats['Макс балл']:.2f}")

    print(f"\n👥 РАСПРЕДЕЛЕНИЕ УЧЕНИКОВ:")
    print(f"   Отличников: {class_stats['Отличник']}")
    print(f"   Хорошистов: {class_stats['Хорошист']}")
    print(f"   Троечников: {class_stats['Троечник']}")
    print(f"   Требуют внимания: {class_stats['Требует внимания']}")

    print(f"\n🏆 ТОП-5 ЛУЧШИХ УЧЕНИКОВ:")
    top = get_top_students(df, 5)
    for i, (_, row) in enumerate(top.iterrows(), 1):
        print(f"   {i}. {row['Ученик']} - {row['Средний_балл']:.2f} ({row['Статус']})")

    struggling = get_struggling_students(df)
    if len(struggling) > 0:
        print(f"\n⚠️  УЧЕНИКИ, ТРЕБУЮЩИЕ ВНИМАНИЯ:")
        for _, row in struggling.iterrows():
            print(f"   • {row['Ученик']} - {row['Средний_балл']:.2f}")
    else:
        print(f"\n✅ Все ученики успевают!")

    print(f"\n📚 СТАТИСТИКА ПО ПРЕДМЕТАМ:")
    for subject, stats in subject_stats.items():
        print(f"   {subject}: среднее = {stats['Средний']:.2f}, мин = {stats['Мин']}, макс = {stats['Макс']}")

    # 5. Сохранение результатов
    print("\n" + "-" * 60)
    print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ...")

    save_to_excel(df)
    create_text_report(df, class_stats, subject_stats)

    # 6. Показать итоговую таблицу
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ ТАБЛИЦА УЧЕНИКОВ:")
    print("=" * 60)
    print(df[['Ученик', 'Средний_балл', 'Статус']].sort_values('Средний_балл', ascending=False).to_string(index=False))

    print("\n✅ Анализ успешно завершён!")
    print("=" * 60)


# ============================================
# ЗАПУСК ПРОГРАММЫ
# ============================================

if __name__ == "__main__":
    main()