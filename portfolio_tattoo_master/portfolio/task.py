from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_email(subject: str, message: str) -> None:
    """
    Sends an email with the provided subject and message.

    Args:
        subject (str): The subject of the email.
        message (str): The body content of the email.

    Returns:
        None
    """
    try:
        # Ensure the EMAIL_HOST_USER is configured
        if not settings.EMAIL_HOST_USER:
            raise ValueError("EMAIL_HOST_USER is not configured in settings.")

        # Sending the email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        logger.info("Email sent successfully.")
    except Exception as e:
        logger.error(f"Error while sending email: {e}")
