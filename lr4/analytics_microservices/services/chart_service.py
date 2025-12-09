import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import io
import base64
from datetime import datetime
import numpy as np


class ChartGenerationService:
    """
    Микросервис для генерации графиков и диаграмм
    """

    @staticmethod
    def generate_bar_chart(labels, values, title="Голосование", x_label="Варианты", y_label="Голосов"):
        """Генерация столбчатой диаграммы"""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Цвета в зависимости от значений
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(values)))

        bars = ax.bar(labels, values, color=colors, edgecolor='black', linewidth=1)

        # Настройки
        ax.set_xlabel(x_label, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_label, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        # Добавляем значения на столбцы
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + (max(values) * 0.01),
                    f'{value}', ha='center', va='bottom', fontsize=10, fontweight='bold')

        # Настройка осей
        ax.set_ylim(0, max(values) * 1.2 if values else 100)

        # Сетка
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)

        # Поворот подписей если нужно
        if len(labels) > 5:
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        # Конвертируем в base64
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        return img_base64

    @staticmethod
    def generate_pie_chart(labels, values, title="Распределение голосов", hole_size=0.3):
        """Генерация круговой диаграммы в формате SVG"""
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
                  '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=hole_size,
            marker=dict(colors=colors[:len(labels)], line=dict(color='white', width=2)),
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='radial',
            hoverinfo='label+value+percent',
            textfont=dict(size=12)
        )])

        fig.update_layout(
            title_text=title,
            title_font_size=18,
            title_font_color='#2C3E50',
            title_x=0.5,
            showlegend=True,
            legend=dict(
                font=dict(size=11),
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.05
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(t=50, b=50, l=50, r=150)
        )

        # Конвертируем в SVG
        svg_bytes = pio.to_image(fig, format='svg', width=800, height=500)
        return svg_bytes.decode('utf-8')

    @staticmethod
    def generate_line_chart(dates, values, title="Активность голосования"):
        """Генерация линейного графика"""
        fig, ax = plt.subplots(figsize=(12, 5))

        # Преобразуем даты если нужно
        if isinstance(dates[0], str):
            dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

        ax.plot(dates, values, marker='o', linewidth=2, markersize=6,
                color='#3498DB', markerfacecolor='#E74C3C')

        # Заполнение под линией
        ax.fill_between(dates, values, alpha=0.3, color='#3498DB')

        # Настройки
        ax.set_xlabel('Дата', fontsize=12, fontweight='bold')
        ax.set_ylabel('Голосов', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        # Сетка
        ax.grid(True, linestyle='--', alpha=0.3)

        # Форматирование дат
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Конвертируем
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        return img_base64

    @staticmethod
    def generate_horizontal_bar_chart(labels, values, title="Сравнение"):
        """Генерация горизонтальной столбчатой диаграммы"""
        fig, ax = plt.subplots(figsize=(10, len(labels) * 0.5 + 2))

        y_pos = np.arange(len(labels))

        bars = ax.barh(y_pos, values, color=plt.cm.coolwarm(np.linspace(0, 1, len(values))))

        # Настройки
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=11)
        ax.set_xlabel('Количество голосов', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        # Добавляем значения
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width + (max(values) * 0.01), bar.get_y() + bar.get_height() / 2,
                    f'{value}', va='center', fontsize=10, fontweight='bold')

        plt.tight_layout()

        # Конвертируем
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        return img_base64