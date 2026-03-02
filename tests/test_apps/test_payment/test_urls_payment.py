from django.test import SimpleTestCase
from django.urls import resolve, reverse

from server.apps.collects.views import CollectViewSet
from server.apps.payment.views import PaymentViewset


class TestUrls(SimpleTestCase):
    """
    Тесты для URL-адресов.
    """

    def test_payment_list_url_resolves(self):
        url = reverse("payment-list")
        self.assertEqual(resolve(url).func.cls, PaymentViewset)
