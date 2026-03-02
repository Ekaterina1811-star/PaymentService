from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from server.apps.collects.models import Collect, Occasion
from server.apps.payment.models import Payment

User = get_user_model()


class TestCollectViewSet(APITestCase):
    """Тесты для CollectViewSet."""

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            username="testuser1",
            email="testuser1@yandex.ru",
            password="SecretPassword"
        )
        cls.user_2 = User.objects.create_user(
            username="testuser2",
            email="testuser2@yandex.ru",
            password="SecretPassword"
        )
        cls.occasion = Occasion.objects.create(name="Test Occasion")
        cls.collect = Collect.objects.create(
            author=cls.user_1,
            name="Test Collect",
            description="Test Description",
            occasion=cls.occasion,
            final_sum=50000,
            completion_datetime=now() + timedelta(days=30),
        )

    def setUp(self):
        self.client = APIClient()

    def get_authenticated_client(self, user):
        """Возвращает аутентифицированный клиент."""
        access_token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(access_token)
        )
        return self.client

    def test_collect_list_unauthenticated(self):
        """Неавторизованный пользователь получает список сборов."""
        url = reverse("collect-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_collect_detail(self):
        """Получение деталей сбора."""
        url = reverse("collect-detail", kwargs={"pk": self.collect.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_collect_authenticated(self):
        """Авторизованный пользователь создаёт сбор."""
        client = self.get_authenticated_client(self.user_1)
        url = reverse("collect-list")
        data = {
            "name": "New Collect",
            "description": "New Description",
            "occasion": self.occasion.pk,
            "final_sum": 50000,
            "completion_datetime": "2028-06-01",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Collect.objects.filter(name="New Collect").exists())

    def test_create_collect_unauthenticated(self):
        """Неавторизованный пользователь не может создать сбор."""
        url = reverse("collect-list")
        data = {
            "name": "New Collect",
            "description": "New Description",
            "occasion": self.occasion.pk,
            "final_sum": 50000,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_collect_by_author(self):
        """Автор может обновить свой сбор."""
        client = self.get_authenticated_client(self.user_1)
        url = reverse("collect-detail", kwargs={"pk": self.collect.pk})
        response = client.patch(url, {"name": "Updated Collect"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_collect_by_another_user(self):
        """Чужой пользователь не может обновить сбор."""
        client = self.get_authenticated_client(self.user_2)
        url = reverse("collect-detail", kwargs={"pk": self.collect.pk})
        response = client.patch(url, {"name": "Updated Collect"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_collect_by_another_user(self):
        """Чужой пользователь не может удалить сбор."""
        client = self.get_authenticated_client(self.user_2)
        url = reverse("collect-detail", kwargs={"pk": self.collect.pk})
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Collect.objects.filter(pk=self.collect.pk).exists())

    def test_delete_collect_by_author(self):
        """Автор может удалить свой сбор."""
        client = self.get_authenticated_client(self.user_1)
        url = reverse("collect-detail", kwargs={"pk": self.collect.pk})
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Collect.objects.filter(pk=self.collect.pk).exists())


class TestOccasionViewSet(APITestCase):
    """Тесты для OccasionViewSet."""
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@yandex.ru",
            password="SecretPassword",
        )
        cls.occasion = Occasion.objects.create(name="Test Occasion")

    def setUp(self):
        self.client = APIClient()

    def get_authenticated_client(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(access_token)
        )
        return self.client

    def test_occasion_list_unauthenticated(self):
        """Неавторизованный пользователь может получить список поводов."""
        url = reverse("occasion-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_occasion_list_authenticated(self):
        """Авторизованный пользователь получает список поводов."""
        client = self.get_authenticated_client()
        url = reverse("occasion-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

