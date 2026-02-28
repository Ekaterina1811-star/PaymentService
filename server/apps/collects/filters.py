import django_filters

from server.apps.collects.models import Collect


class CollectFilter(django_filters.FilterSet):
    """
    Фильтр для сборов.
    Осуществляет фильтрацию по id автора,
    дате создания

    Attributes:
    - author: Фильтр по id автора сбора средств.
    - ordering: Фильтр для сортировки результатов по дате создания
    """
    author = django_filters.NumberFilter(field_name="author")
    ordering = django_filters.OrderingFilter(field_name="created_at")

    class Meta:
        model = Collect
        fields = ("author", "created_at",)
