import os

import structlog
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from server.apps.collects.models import Collect
from server.apps.core.email import create_collect_confirmation_email


DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
logger = structlog.get_logger(__name__)
User = get_user_model()


@shared_task
def send_collect_confirmation_task(user_id, collect_id):
    """
    Отправляет сообщение на электронную почту при создании сбора
    :param user_id: id получателя.
    :param collect_id: Id денежного сбора.
    """
    user = User.objects.filter(id=user_id).first()
    collect_instance = Collect.objects.filter(id=collect_id).first()
    if user and collect_instance:
        email_message = create_collect_confirmation_email(
            user.username,
            collect_instance.name,
            collect_instance.description,
            collect_instance.final_sum,
            collect_instance.completion_datetime,
        )
        send_mail(
            "Payment Service: Групповые денежные сборы",
            email_message,
            DEFAULT_FROM_EMAIL, # Адрес почты, с которой будут отправляться письма
            [user.email],
            fail_silently=False,
        )
    else:
        if not user:
            logger.info("User not found", user_id=user_id)
        if not collect_instance:
            logger.info("Collect not found", collect_id=collect_id)
