import csv
import json
import pandas as pd
from io import StringIO, BytesIO
from datetime import datetime
import xlsxwriter


class DataExportService:
    """
    Микросервис для экспорта данных в различные форматы
    """

    @staticmethod
    def export_to_csv(data, filename="export"):
        """Экспорт в CSV формат"""
        output = StringIO()
        writer = csv.writer(output)

        # Определяем структуру данных
        if isinstance(data, list) and data:
            # Если это список словарей
            if isinstance(data[0], dict):
                # Заголовки
                headers = data[0].keys()
                writer.writerow(headers)

                # Данные
                for row in data:
                    writer.writerow([row.get(header, '') for header in headers])
            else:
                # Простой список
                for row in data:
                    writer.writerow([row])
        elif isinstance(data, dict):
            # Словарь
            writer.writerow(['Key', 'Value'])
            for key, value in data.items():
                writer.writerow([key, str(value)])

        return output.getvalue()

    @staticmethod
    def export_to_json(data, indent=2):
        """Экспорт в JSON формат"""
        return json.dumps(data, indent=indent, ensure_ascii=False, default=str)

    @staticmethod
    def export_to_excel(data, sheet_name="Data"):
        """Экспорт в Excel формат"""
        output = BytesIO()

        # Создаем DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame()

        # Записываем в Excel
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Настройка формата
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            # Автоширина колонок
            for i, col in enumerate(df.columns):
                column_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                worksheet.set_column(i, i, column_len)

        output.seek(0)
        return output.getvalue()

    @staticmethod
    def export_poll_results(poll_data, format='csv'):
        """Экспорт результатов конкретного голосования"""
        if not poll_data:
            return None

        if format.lower() == 'json':
            return DataExportService.export_to_json(poll_data)

        elif format.lower() == 'csv':
            output = StringIO()
            writer = csv.writer(output)

            # Заголовок
            writer.writerow(['Статистика голосования'])
            writer.writerow(['ID голосования', poll_data['poll']['id']])
            writer.writerow(['Название', poll_data['poll']['title']])
            writer.writerow(['Дата создания', poll_data['poll']['created_at']])
            writer.writerow(['Всего голосов', poll_data['poll']['total_votes']])
            writer.writerow([])

            # Результаты по вариантам
            writer.writerow(['Результаты по вариантам ответа'])
            writer.writerow(['Вариант ответа', 'Голосов', 'Процент (%)'])

            for choice in poll_data['choices']:
                writer.writerow([
                    choice['choice_text'],
                    choice['votes_count'],
                    choice['percentage']
                ])

            return output.getvalue()

        elif format.lower() == 'excel':
            # Подготовка данных для Excel
            excel_data = {
                'poll_info': [
                    ['ID голосования', poll_data['poll']['id']],
                    ['Название', poll_data['poll']['title']],
                    ['Дата создания', poll_data['poll']['created_at']],
                    ['Всего голосов', poll_data['poll']['total_votes']]
                ],
                'choices': [[
                    'Вариант ответа', 'Голосов', 'Процент (%)'
                ]] + [[
                    choice['choice_text'],
                    choice['votes_count'],
                    choice['percentage']
                ] for choice in poll_data['choices']]
            }

            return DataExportService.export_to_excel(excel_data)

    @staticmethod
    def export_polls_summary(polls_data, format='csv'):
        """Экспорт сводки по всем голосованиям"""
        if format.lower() == 'json':
            return DataExportService.export_to_json(polls_data)

        elif format.lower() == 'csv':
            output = StringIO()
            writer = csv.writer(output)

            # Сводная информация
            writer.writerow(['Сводная статистика голосований'])
            writer.writerow(['Всего голосований', polls_data['summary']['total_polls']])
            writer.writerow(['Всего голосов', polls_data['summary']['total_votes']])
            writer.writerow(['Среднее голосов на голосование',
                             polls_data['summary']['average_votes_per_poll']])
            writer.writerow(['Активных голосований', polls_data['summary']['active_polls']])
            writer.writerow([])

            # Список голосований
            writer.writerow(['Список голосований'])
            writer.writerow(['ID', 'Название', 'Дата создания', 'Голосов', 'Вариантов', 'Статус'])

            for poll in polls_data['polls']:
                writer.writerow([
                    poll['id'],
                    poll['title'],
                    poll['created_at'],
                    poll['vote_count'],
                    poll['choices_count'],
                    'Активно' if poll['is_active'] else 'Неактивно'
                ])

            return output.getvalue()