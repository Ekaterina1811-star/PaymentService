from django.core.cache import cache
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from server.apps.payment.filters import PaymentFilter
from server.apps.payment.models import Payment
from server.apps.payment.serializers import PaymentSerializer
from server.apps.payment.tasks import send_payment_confirmation_task
from server.apps.core.email import create_payment_confirmation_email


class PaymentViewset(viewsets.ModelViewSet):
    """
    ViewSet для работы с платежами.

    Этот ViewSet предоставляет эндпоинты для управления платежами.

    Attributes:
        - queryset: Запрос, возвращающий все объекты Payment.
        - serializer_class: Сериализатор, используемый для преобразования
        данных платежей.
        - filterset_class: Класс фильтра для применения фильтрации к запросу.

    Permissions:
        - get_permissions: Метод для определения разрешений в зависимости
        от действия.

    Methods:
        - perform_create(self, serializer): Создает новый платеж и отправляет
        подтверждение по электронной почте.
        - perform_update(self, serializer): Обновляет данные о платеже.
        - perform_destroy(self, instance): Удаляет платеж.
    """
    queryset = Payment.objects.order_by("-created_at")
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter


    def get_permissions(self):
        """
        Возвращает разрешения в зависимости от действия
        """
        action_permissions = {
            "list": (permissions.AllowAny(),),
            "retrieve": (permissions.AllowAny(),),
            "create": (permissions.IsAuthenticated(),),
            "update": (permissions.IsAdminUser(),),
            "partial_update": (permissions.IsAdminUser(),),
            "destroy": (permissions.IsAdminUser(),),
        }
        return action_permissions.get(self.action, super().get_permissions())


    def list(self, request, *args, **kwargs):
        """
        Возвращает список платежей с применением кэширования.
        """
        cache_key = "payments_list"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60 * 15)
        return response


    def perform_create(self, serializer):
        """
        Создает новый платеж и отпрравляет email
        :param serializer: Сериализатор для сбора средств.
        """
        user = self.request.user
        payment = serializer.save(contributor=user)
        user_email = user.email
        collect_instance = serializer.validated_data["collect"]
        paid_sum = serializer.validated_data["sum"]
        email_message = create_payment_confirmation_email(
            user.first_name,
            collect_instance.name,
            paid_sum,
        )
        send_payment_confirmation_task(self.request.user.id, payment.id)
        cache.delete("payments_list")
        cache.delete("collects_list")


    def perform_update(self, serializer):
        """
        Обновляет данные платежа
        :param serializer: Сериализатор для сбора средств.
        """
        try:
            serializer.save() # Сохраняем обновленный платеж
            cache.delete("payments_list")
            cache.delete("collects_list")
        except Exception as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)


    def perform_destroy(self, instance):
        """
        Удаляет платеж
        :param instance: Экземпляр сбора средств.
        """
        try:
            instance.delete()
            cache.delete("payments_list")
        except Exception as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

