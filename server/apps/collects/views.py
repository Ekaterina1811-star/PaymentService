from django.core.cache import cache
from django.db.models import Sum, Count
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from server.apps.collects.filters import CollectFilter
from server.apps.collects.models import Collect, Occasion
from server.apps.collects.serializers import CollectSerializer, OccasionSerializer
from server.apps.collects.tasks import send_collect_confirmation_task
from server.apps.core.pagination import CustomPagination
from server.apps.core.permissions import OwnerOrReadOnly


class OccasionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для просмотра поводов сборов
    """
    queryset = Occasion.objects.all()
    serializer_class = OccasionSerializer
    permission_classes = (OwnerOrReadOnly,)


class CollectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы со сборами средств.
    Этот ViewSet предоставляет эндпоинты для управления сборами средств.

    Attributes:
        - queryset: Запрос, возвращающий все объекты Collect.
        - serializer_class: Сериализатор, используемый для преобразования
        данных сбора средств.
        - pagination_class: Класс пагинации для разбиения результатов
        на страницы.
        - filterset_class: Класс фильтра для применения фильтрации к запросу.

    Permissions:
        - get_permissions: Метод для определения разрешений в зависимости
        от действия.

    Methods:
        - perform_create(self, serializer): Создает новый сбор
        и отправляет подтверждение по электронной почте.
        - perform_update(self, serializer): Обновляет данные о сборе.
        - perform_destroy(self, instance): Удаляет сбор.
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    filterset_class = CollectFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Переопределяем queryset, чтобы для каждого сбора
        посчитать собранную сумму и количество участников.
        """
        return Collect.objects.annotate(
            # Создаём новое поле 'current_sum', считая сумму всех полей 'sum'
            # у связанных платежей. 'payment' — это related_name у ForeignKey в модели Payment.
            current_sum=Sum('payment__sum'),
            # Считаем количество уникальных участников. distinct=True,
            # чтобы один и тот же человек не посчитался дважды.
            contributors_count=Count('payment__contributor', distinct=True)
        ).order_by('-created_at')

    def get_permissions(self):
        """
        Возвращает разрешения в зависимости от действия
        """
        action_permissions = {
            "list": (permissions.AllowAny(),),
            "retrieve": (permissions.AllowAny(),),
            "create": (permissions.IsAuthenticated(),),
            "update": (OwnerOrReadOnly(),),
            "partial_update": (OwnerOrReadOnly(),),
            "destroy": (OwnerOrReadOnly(),),
        }
        return action_permissions.get(self.action, super().get_permissions())

    def list(self, request, *args, **kwargs):
        """
        Возвращает список сборов средств с применением кэширования
        """
        # Придумываем уникальный ключ для кэша
        cache_key = "collects_list"
        # Получаем данные из кэша
        cached_data = cache.get(cache_key)
        if cached_data:
            # Если данные есть в кэше, возвращаем их
            return Response(cached_data)
        # Если в кэше ничего нет
        response = super().list(request, *args, **kwargs)
        # Сохраняем результат в кэш на 15 минут перед тем, как его отдать
        cache.set(cache_key, response.data, 60 * 15)
        return response

    def perform_create(self, serializer):
        """Создает сбор"""
        user = self.request.user
        collect_instance = serializer.save(author=user)
        send_collect_confirmation_task.delay(
            user_id=user.id,
            collect_id=collect_instance.id
        )
        cache.delete("collects_list")

    def perform_update(self, serializer):
        """Обновляет данные о денежном сборе"""
        try:
            serializer.save()
            cache.delete("collects_list")

        except Exception as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        """Удаляет денежный сбор"""
        try:
            instance.delete()
            cache.delete("collects_list")
        except Exception as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
