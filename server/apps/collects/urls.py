from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server.apps.collects.views import CollectViewSet, OccasionViewSet


router = DefaultRouter()

router.register(r"collect", CollectViewSet)
router.register(r"occasion", OccasionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

# Зарегать пользователя http://127.0.0.1:8000/auth/users/
# http://127.0.0.1:8000/auth/jwt/create/ получаем токен
# создаем повод
# http://127.0.0.1:8000/occasion/
