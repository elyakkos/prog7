from django.db.models import Q
from datetime import datetime, timedelta


class FilterService:
    """
    Микросервис для фильтрации и сортировки данных
    """

    def __init__(self, poll_model):
        self.Poll = poll_model

    def apply_filters(self, filters):
        """Применение всех фильтров и сортировки"""
        queryset = self.Poll.objects.all()

        # Фильтрация по дате создания
        queryset = self._filter_by_date(queryset, filters)

        # Фильтрация по активности
        queryset = self._filter_by_activity(queryset, filters)

        # Фильтрация по количеству голосов
        queryset = self._filter_by_votes(queryset, filters)

        # Фильтрация по тексту
        queryset = self._filter_by_text(queryset, filters)

        # Сортировка
        queryset = self._apply_sorting(queryset, filters)

        # Лимит
        queryset = self._apply_limit(queryset, filters)

        return queryset

    def _filter_by_date(self, queryset, filters):
        """Фильтрация по дате"""
        if filters.get('start_date'):
            queryset = queryset.filter(created_at__gte=filters['start_date'])

        if filters.get('end_date'):
            queryset = queryset.filter(created_at__lte=filters['end_date'])

        # Фильтр за последние N дней
        if filters.get('last_days'):
            try:
                days = int(filters['last_days'])
                date_from = datetime.now() - timedelta(days=days)
                queryset = queryset.filter(created_at__gte=date_from)
            except ValueError:
                pass

        return queryset

    def _filter_by_activity(self, queryset, filters):
        """Фильтрация по активности"""
        if filters.get('is_active') is not None:
            queryset = queryset.filter(is_active=filters['is_active'])

        if filters.get('has_votes') is not None:
            if filters['has_votes']:
                queryset = queryset.filter(votes__isnull=False).distinct()
            else:
                queryset = queryset.filter(votes__isnull=True)

        return queryset

    def _filter_by_votes(self, queryset, filters):
        """Фильтрация по количеству голосов"""
        if filters.get('min_votes'):
            queryset = queryset.annotate(
                vote_count=Count('votes')
            ).filter(vote_count__gte=filters['min_votes'])

        if filters.get('max_votes'):
            queryset = queryset.annotate(
                vote_count=Count('votes')
            ).filter(vote_count__lte=filters['max_votes'])

        return queryset

    def _filter_by_text(self, queryset, filters):
        """Фильтрация по тексту"""
        search_text = filters.get('search', '').strip()

        if search_text:
            queryset = queryset.filter(
                Q(title__icontains=search_text) |
                Q(description__icontains=search_text)
            )

        return queryset

    def _apply_sorting(self, queryset, filters):
        """Применение сортировки"""
        sort_by = filters.get('sort_by', '-created_at')
        sort_order = filters.get('sort_order', 'desc')

        sort_map = {
            'date': 'created_at',
            'title': 'title',
            'popularity': 'vote_count',
            'votes': 'vote_count',
            'choices': 'choices_count'
        }

        # Преобразуем человекочитаемый ключ в поле модели
        field_name = sort_map.get(sort_by, sort_by)

        # Если нужна сортировка по количеству голосов или вариантов
        if field_name in ['vote_count', 'choices_count']:
            queryset = queryset.annotate(**{field_name: Count(field_name[:-6])})

        # Определяем направление сортировки
        if sort_order == 'asc':
            order_field = field_name
        else:
            order_field = f'-{field_name}'

        return queryset.order_by(order_field)

    def _apply_limit(self, queryset, filters):
        """Применение лимита"""
        limit = filters.get('limit')
        if limit:
            try:
                limit = int(limit)
                if limit > 0:
                    queryset = queryset[:limit]
            except ValueError:
                pass

        return queryset

    def get_filter_options(self):
        """Получение доступных опций фильтрации"""
        from django.db.models import Min, Max, Count

        stats = self.Poll.objects.aggregate(
            min_date=Min('created_at'),
            max_date=Max('created_at'),
            total_polls=Count('id'),
            active_polls=Count('id', filter=Q(is_active=True))
        )

        # Получаем уникальные годы для фильтрации
        years = self.Poll.objects.dates('created_at', 'year')

        return {
            'date_range': {
                'min': stats['min_date'],
                'max': stats['max_date']
            },
            'years': [year.year for year in years],
            'counts': {
                'total': stats['total_polls'],
                'active': stats['active_polls'],
                'inactive': stats['total_polls'] - stats['active_polls']
            },
            'available_filters': [
                {'key': 'start_date', 'type': 'date', 'label': 'Дата от'},
                {'key': 'end_date', 'type': 'date', 'label': 'Дата до'},
                {'key': 'last_days', 'type': 'number', 'label': 'За последние дней'},
                {'key': 'is_active', 'type': 'boolean', 'label': 'Только активные'},
                {'key': 'has_votes', 'type': 'boolean', 'label': 'С голосами'},
                {'key': 'min_votes', 'type': 'number', 'label': 'Минимум голосов'},
                {'key': 'max_votes', 'type': 'number', 'label': 'Максимум голосов'},
                {'key': 'search', 'type': 'text', 'label': 'Поиск по тексту'},
                {'key': 'sort_by', 'type': 'select', 'label': 'Сортировать по',
                 'options': [
                     {'value': 'date', 'label': 'Дате'},
                     {'value': 'title', 'label': 'Названию'},
                     {'value': 'popularity', 'label': 'Популярности'},
                     {'value': 'choices', 'label': 'Количеству вариантов'}
                 ]},
                {'key': 'sort_order', 'type': 'select', 'label': 'Порядок сортировки',
                 'options': [
                     {'value': 'desc', 'label': 'По убыванию'},
                     {'value': 'asc', 'label': 'По возрастанию'}
                 ]}
            ]
        }