from django.contrib.auth import get_user_model
from django.db import models

from server.apps.collects.models import Collect
from server.apps.core.models import CreateUpdateDateModelMixin


User = get_user_model()


class Payment(CreateUpdateDateModelMixin):
    """
    Модель платежа
    """
    contributor = models.ForeignKey(
        User,
        verbose_name="Вкладчик",
        related_name="payment",
        on_delete=models.PROTECT,
    )
    collect = models.ForeignKey(
        Collect,
        verbose_name="Сбор",
        on_delete=models.PROTECT,
        related_name="payment",
    )

    sum = models.DecimalField(
        verbose_name="Сумма, которую собрали",
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return (
            f"Платеж {self.id}. "
            f"Платеж внес {self.contributor_id}. "
            f"Сумма платежа {self.sum}. "
            f"Дата платежа {self.created_at}. "
            f"Сбор {self.collect_id}"
        )


