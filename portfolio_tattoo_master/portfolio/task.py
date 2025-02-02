from typing import Dict, Any
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email(data: Dict[str, Any]) -> None:
    """
    Sends an email with the provided user data.

    Args:
        data (Dict[str, Any]): A dictionary containing user details, including:
            - 'name' (str): The sender's name.
            - 'email' (str): The sender's email.
            - 'message' (str): The main message content.
            - Optional: 'telegram' (str): The sender's Telegram handle.
            - Optional: 'whatsapp' (str): The sender's WhatsApp number.

    Returns:
        None
    """
    name: str = data.get('name', 'Anonymous')
    email: str = data.get('email', 'No email provided')
    message: str = data.get('message', '')

    # Append additional contact information
    contact_info = [f"My email: {email}"]
    if telegram := data.get("telegram"):
        contact_info.append(f"My Telegram: {telegram}")
    if whatsapp := data.get("whatsapp"):
        contact_info.append(f"My WhatsApp: {whatsapp}")

    full_message = f"{message}\n\n" + "\n".join(contact_info)

    try:
        send_mail(
            subject=f"I want a tattoo - {name}",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error while sending email: {e}")
