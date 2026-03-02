from django.test import SimpleTestCase
from django.urls import resolve, reverse

from server.apps.collects.views import CollectViewSet, OccasionViewSet


class TestUrls(SimpleTestCase):
    """
    Тесты для URL-адресов.
    """

    def test_occasions_list_url_resolves(self):
        url = reverse("occasion-list")
        self.assertEqual(resolve(url).func.cls, OccasionViewSet)
