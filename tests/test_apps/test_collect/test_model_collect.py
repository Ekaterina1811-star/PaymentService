from django.contrib.auth import get_user_model
from django.db.models import CharField, DateField, DateTimeField, ForeignKey, TextField
from pytest import mark

from server.apps.collects.models import Collect, Occasion
from server.apps.payment.models import Payment

User = get_user_model()


@mark.django_db
class TestOccasionModel:
    """Тесты для модели Occasion"""
    def test_str_representation(self):
        occasion = Occasion.objects.create(name="Test Occasion")
        assert str(occasion) == "Test Occasion"


@mark.django_db
class TestCollectModel:
    """Тесты для модели Collect"""
    def test_model_fields(self):
        fields = Collect._meta.fields
        field_names = [field.name for field in fields]
        assert "author" in field_names
        assert "name" in field_names
        assert "occasion" in field_names
        assert "description" in field_names
        assert "final_sum" in field_names
        assert "collect_image" in field_names
        assert "completion_datetime" in field_names
        assert "created_at" in field_names

    def test_field_types(self):
        assert isinstance(Collect._meta.get_field("author"), ForeignKey)
        assert isinstance(Collect._meta.get_field("name"), CharField)
        assert isinstance(Collect._meta.get_field("occasion"), ForeignKey)
        assert isinstance(Collect._meta.get_field("description"), TextField)
        assert isinstance(Collect._meta.get_field("completion_datetime"), DateField)
        assert isinstance(Collect._meta.get_field("created_at"), DateField)

