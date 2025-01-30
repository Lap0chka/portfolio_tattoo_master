from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email(data):
    name = data['name']
    email = data['email']
    message = data['message']
    message += f'\nMy email: {email}'
    if data.get('telegram'):
        message += f'\nMy telegram: {data["telegram"]}'
    if data.get('whatsapp'):
        message += f'\nMy whatsapp: {data["whatsapp"]}'

    try:
        send_mail(
            subject=f'I want a tattoo - {name}',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error while sending email: {e}")
