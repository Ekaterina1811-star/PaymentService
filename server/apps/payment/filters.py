import django_filters

from server.apps.payment.models import Payment


class PaymentFilter(django_filters.FilterSet):
    """
    Фильтр для платежей.
    Осуществляет фильтрацию по id денежного сбора,
    дате создания, участнику
    Attributes:
    - collect_id: Фильтр по id денежного сбора.
    - ordering: Фильтр для сортировки результатов по дате
    создания и участнику.
    """
    collect_id = django_filters.NumberFilter(field_name="collect_id")
    ordering = django_filters.OrderingFilter(
        fields=["created_at", "contributor"]
    )
    class Meta:
        model = Payment
        fields = (
            "collect_id",
            "created_at",
            "contributor",
        )
