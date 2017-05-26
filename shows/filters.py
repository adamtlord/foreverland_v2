import datetime
import django_filters
from shows.models import Show


class ShowFilter(django_filters.FilterSet):
    upcoming = django_filters.BooleanFilter(name='upcoming', method='get_upcoming_shows')

    class Meta:
        model = Show
        fields = ['public', 'upcoming']

    def get_upcoming_shows(self, queryset, name, value):
        now = datetime.datetime.now()
        key = 'date__{}'.format('gt' if value else 'lt')
        return queryset.filter(**{
            key: now
        })
