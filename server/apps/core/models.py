from django.db import models


class CreateUpdateDateModelMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата изменения",
        auto_now_add=True,
    )
