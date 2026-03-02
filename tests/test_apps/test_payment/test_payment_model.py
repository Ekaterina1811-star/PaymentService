from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from pytest import mark

from server.apps.collects.models import Collect, Occasion
from server.apps.payment.models import Payment


User = get_user_model()


@mark.django_db
class TestPaymentModel:

    def test_model_fields(self):
        fields = Payment._meta.fields
        field_names = [field.name for field in fields]
        assert "contributor" in field_names
        assert "collect" in field_names
        assert "sum" in field_names
        assert "created_at" in field_names

    def test_str_representation(self):
        user = User.objects.create(
            username="test_user",
            email="test@test.com",
            password="TestPass123"
        )
        occasion = Occasion.objects.create(name="Test Occasion")
        collect = Collect.objects.create(
            author=user,
            name="Test Collect",
            occasion=occasion,
            description="Testing",
            final_sum=1000,
            completion_datetime=now() + timedelta(days=30),
        )
        payment = Payment.objects.create(
            contributor=user,
            collect=collect,
            sum=100,
        )
        assert str(payment) == (
            f"Платеж {payment.id}. "
            f"Платеж внес {payment.contributor_id}. "
            f"Сумма платежа {payment.sum}. "
            f"Дата платежа {payment.created_at}. "
            f"Сбор {payment.collect_id}"
        )
