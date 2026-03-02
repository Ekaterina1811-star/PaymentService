import os

import structlog
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from server.apps.core.email import create_payment_confirmation_email
from server.apps.payment.models import Payment


DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
logger = structlog.get_logger(__name__)
User = get_user_model()


@shared_task
def send_payment_confirmation_task(user_id, payment_id):
    """
    Асинхронная задача отправки электронного сообщения.
    Отправляет электронное сообщение на указанный адрес.

    :param user_id: Id получателя.
    :param payment_id: Id платежа.
    """
    user = User.objects.filter(id=user_id).first()
    payment = Payment.objects.filter(id=payment_id).first()
    if user and payment:
        email_message = create_payment_confirmation_email(
            user.username,
            payment.collect.name,
            payment.sum,
        )
        send_mail(
            "Payment Service: Групповые денежные сборы",
            email_message,
            DEFAULT_FROM_EMAIL,  # Адрес почты, с которой будут отправляться письма
            [user.email],
            fail_silently=False,
        )
    else:
        if not user:
            logger.info("User not found", user_id=user_id)
        if not payment:
            logger.info("Payment not found", payment_id=payment_id)
