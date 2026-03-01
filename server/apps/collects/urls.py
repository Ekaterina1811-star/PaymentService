from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server.apps.collects.views import CollectViewSet, OccasionViewSet


router = DefaultRouter()


router.register(r"server.apps.collects", CollectViewSet)
router.register(r"server.apps.occasion", OccasionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

