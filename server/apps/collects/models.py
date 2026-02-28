from django.contrib.auth import get_user_model
from django.db import models

from server.apps.core.models import CreateUpdateDateModelMixin


User = get_user_model()


class Occasion(models.Model):
    """
    Модель для поводов сборов
    """
    name = models.CharField(
        max_length=20,
        verbose_name="Название повода"
    )


    def __str__(self):
        return self.name


class Collect(CreateUpdateDateModelMixin):
    """
    Модель для групповых денежных сборов
    """
    name = models.CharField(
        max_length=20,
        verbose_name="Название сбора"
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор сбора",
        related_name="collects",
        on_delete=models.PROTECT
    )
    description = models.TextField(verbose_name="Описание")
    occasion = models.ForeignKey(
        Occasion,
        verbose_name="Повод сбора",
        related_name="collects",
        on_delete=models.CASCADE,
    )
    final_sum = models.DecimalField(
        verbose_name="Необходимая сумма",
        max_digits=12,
        decimal_places=2,
    )
    collect_image = models.ImageField(
        upload_to="media",
        null=True,
        default=None,
    )
    completion_datetime = models.DateField(verbose_name="Дата завершения сбора")

    def __str__(self):
        return self.name
