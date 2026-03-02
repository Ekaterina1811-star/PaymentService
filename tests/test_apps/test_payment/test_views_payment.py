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


class TestPaymentViewSet(APITestCase):
    """Тесты для PaymentViewSet."""
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            username="testuser1",
            email="testuser1@yandex.ru",
            password="SecretPassword",
        )
        cls.user_2 = User.objects.create_user(
            username="testuser2",
            email="testuser2@yandex.ru",
            password="SecretPassword",
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
        cls.payment = Payment.objects.create(
            contributor=cls.user_1,
            collect=cls.collect,
            sum=100,                    # amount → sum
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

    def test_payment_list(self):
        """Список платежей доступен без авторизации."""
        url = reverse("payment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_detail(self):
        """Детали платежа доступны без авторизации."""
        url = reverse("payment-detail", kwargs={"pk": self.payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payment_authenticated(self):
        """Авторизованный пользователь создаёт платёж."""
        client = self.get_authenticated_client(self.user_1)
        url = reverse("payment-list")
        data = {
            "collect": self.collect.pk,
            "sum": 50,
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Payment.objects.filter(sum=50).exists())

    def test_create_payment_unauthenticated(self):
        """Неавторизованный пользователь не может создать платёж."""
        url = reverse("payment-list")
        data = {
            "collect": self.collect.pk,
            "sum": 50,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_payment_by_author(self):
        """Платёж нельзя изменить даже автору."""
        client = self.get_authenticated_client(self.user_1)
        url = reverse("payment-detail", kwargs={"pk": self.payment.pk})
        response = client.patch(url, {"sum": 200})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.payment.refresh_from_db()
        self.assertNotEqual(self.payment.sum, 200)

    def test_update_payment_by_another_user(self):
        """Чужой пользователь не может изменить платёж."""
        client = self.get_authenticated_client(self.user_2)
        url = reverse("payment-detail", kwargs={"pk": self.payment.pk})
        response = client.patch(url, {"sum": 200})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_payment_by_another_user(self):
        """Чужой пользователь не может удалить платёж."""
        client = self.get_authenticated_client(self.user_2)
        url = reverse("payment-detail", kwargs={"pk": self.payment.pk})
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Payment.objects.filter(pk=self.payment.pk).exists())

    def test_delete_payment_by_author(self):
        """Автор тоже не может удалить платёж."""
        client = self.get_authenticated_client(self.user_1)
        url = reverse("payment-detail", kwargs={"pk": self.payment.pk})
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Payment.objects.filter(pk=self.payment.pk).exists())
