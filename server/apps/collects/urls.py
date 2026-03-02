from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server.apps.collects.views import CollectViewSet, OccasionViewSet


router = DefaultRouter()


router.register(r"collects", CollectViewSet)
router.register(r"occasion", OccasionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

