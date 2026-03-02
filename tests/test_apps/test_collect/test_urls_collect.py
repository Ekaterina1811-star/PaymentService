from django.test import SimpleTestCase
from django.urls import resolve, reverse

from server.apps.collects.views import CollectViewSet


class TestUrls(SimpleTestCase):
    """
    Тесты для URL-адресов.
    """

    def test_collect_list_url_resolves(self):
        url = reverse("collect-list")
        self.assertEqual(resolve(url).func.cls, CollectViewSet)

