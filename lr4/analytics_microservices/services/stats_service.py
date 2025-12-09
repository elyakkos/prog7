from django.db.models import Count, F, Q
from datetime import datetime, timedelta
import math


class PollStatisticsService:
    """
    Микросервис для сбора статистики по голосованиям
    """

    def __init__(self, poll_model, vote_model):
        self.Poll = poll_model
        self.Vote = vote_model

    def get_basic_stats(self, poll_id):
        """Базовая статистика по голосованию"""
        try:
            poll = self.Poll.objects.get(id=poll_id)
        except self.Poll.DoesNotExist:
            return None

        votes_count = self.Vote.objects.filter(poll=poll).count()

        # Статистика по вариантам
        choices_stats = []
        for choice in poll.choices.all():
            choice_votes = self.Vote.objects.filter(choice=choice).count()
            percentage = (choice_votes / votes_count * 100) if votes_count > 0 else 0

            choices_stats.append({
                'choice_id': choice.id,
                'choice_text': choice.choice_text,
                'votes_count': choice_votes,
                'percentage': round(percentage, 2)
            })

        return {
            'poll': {
                'id': poll.id,
                'title': poll.title,
                'description': poll.description,
                'created_at': poll.created_at,
                'total_votes': votes_count,
                'choices_count': poll.choices.count()
            },
            'choices': choices_stats
        }

    def get_aggregated_stats(self, filters=None):
        """Агрегированная статистика по всем голосованиям"""
        queryset = self.Poll.objects.all()

        # Применяем фильтры
        if filters:
            queryset = self._apply_filters(queryset, filters)

        # Основная статистика
        total_polls = queryset.count()

        # Аннотируем количество голосов
        polls_with_votes = queryset.annotate(
            vote_count=Count('votes'),
            choices_count=Count('choices')
        )

        # Суммарная статистика
        total_votes = sum(poll.vote_count for poll in polls_with_votes)
        avg_votes = total_votes / total_polls if total_polls > 0 else 0

        # Подготовка данных
        polls_data = []
        for poll in polls_with_votes:
            polls_data.append({
                'id': poll.id,
                'title': poll.title,
                'created_at': poll.created_at,
                'vote_count': poll.vote_count,
                'choices_count': poll.choices_count,
                'is_active': poll.is_active
            })

        return {
            'summary': {
                'total_polls': total_polls,
                'total_votes': total_votes,
                'average_votes_per_poll': round(avg_votes, 2),
                'active_polls': queryset.filter(is_active=True).count()
            },
            'polls': polls_data,
            'filters_applied': filters or {}
        }

    def get_vote_distribution(self, poll_id):
        """Распределение голосов по времени"""
        poll_votes = self.Vote.objects.filter(poll_id=poll_id)

        # По дням
        by_day = poll_votes.extra(
            select={'day': "date(voted_at)"}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')

        # По часам (за последние 24 часа)
        last_24h = datetime.now() - timedelta(hours=24)
        recent_votes = poll_votes.filter(voted_at__gte=last_24h)

        by_hour = []
        for hour in range(24):
            hour_start = last_24h.replace(hour=hour, minute=0, second=0, microsecond=0)
            hour_end = hour_start + timedelta(hours=1)

            count = recent_votes.filter(
                voted_at__gte=hour_start,
                voted_at__lt=hour_end
            ).count()

            by_hour.append({
                'hour': f"{hour:02d}:00",
                'count': count
            })

        return {
            'by_day': list(by_day),
            'by_hour': by_hour,
            'last_24h_total': recent_votes.count()
        }

    def get_popular_polls(self, limit=10, period_days=None):
        """Самые популярные голосования"""
        queryset = self.Poll.objects.annotate(
            vote_count=Count('votes')
        ).order_by('-vote_count')

        if period_days:
            date_from = datetime.now() - timedelta(days=period_days)
            queryset = queryset.filter(created_at__gte=date_from)

        polls = queryset[:limit]

        result = []
        for poll in polls:
            result.append({
                'id': poll.id,
                'title': poll.title,
                'vote_count': poll.vote_count,
                'created_at': poll.created_at,
                'vote_percentage': self._calculate_popularity_percentage(poll.vote_count)
            })

        return result

    def _apply_filters(self, queryset, filters):
        """Применение фильтров к запросу"""
        # Фильтр по дате
        if filters.get('start_date'):
            queryset = queryset.filter(created_at__gte=filters['start_date'])
        if filters.get('end_date'):
            queryset = queryset.filter(created_at__lte=filters['end_date'])

        # Фильтр по активности
        if filters.get('is_active') is not None:
            queryset = queryset.filter(is_active=filters['is_active'])

        # Фильтр по минимальному количеству голосов
        if filters.get('min_votes'):
            queryset = queryset.annotate(
                vote_count=Count('votes')
            ).filter(vote_count__gte=filters['min_votes'])

        # Сортировка
        sort_by = filters.get('sort_by', '-created_at')
        if sort_by == 'popularity':
            queryset = queryset.annotate(
                vote_count=Count('votes')
            ).order_by('-vote_count')
        elif sort_by == 'title':
            queryset = queryset.order_by('title')
        elif sort_by == '-title':
            queryset = queryset.order_by('-title')
        else:
            queryset = queryset.order_by(sort_by)

        return queryset

    def _calculate_popularity_percentage(self, vote_count):
        """Расчет процентной популярности"""
        # Базовый расчет, можно адаптировать
        max_votes = self.Poll.objects.annotate(
            vote_count=Count('votes')
        ).aggregate(max=Count('votes'))['max'] or 1

        return round((vote_count / max_votes) * 100, 2) if max_votes > 0 else 0