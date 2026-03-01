from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server.apps.payment.views import PaymentViewset


router = DefaultRouter()


router.register(r"server.apps.payment", PaymentViewset)

urlpatterns = [
    path("", include(router.urls)),
]
