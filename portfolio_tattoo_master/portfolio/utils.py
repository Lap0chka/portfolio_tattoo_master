from typing import Type, Dict, Any

from django.contrib import messages
from django.core.cache import cache
from django.db.models import Model, QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext as _

from .form import FeedbackForm
from .models import MainImage, PortfolioImage
from .task import send_email


def get_cached_images(cache_key: str, model: Type[Model], timeout: int = 60 * 30) -> QuerySet:
    """
    Retrieves images from cache or database.

    Args:
        cache_key (str): The cache key to store/retrieve images.
        model (models.Model): The Django model to fetch images from.
        timeout (int, optional): Cache timeout in seconds. Default is 30 minutes.

    Returns:
        QuerySet: A queryset containing images.
    """
    images = cache.get(cache_key)
    if not images:
        images = model.objects.all()
        cache.set(cache_key, images, timeout=timeout)

    return images

def get_images() -> QuerySet[MainImage]:
    """
    Retrieves cached images for the main image gallery.

    Returns:
        QuerySet[MainImage]: A queryset containing cached main images.
    """
    return get_cached_images("main_images", MainImage)


def get_portfolio_images() -> QuerySet[PortfolioImage]:
    """
    Retrieves cached images for the portfolio gallery.

    Returns:
        QuerySet[PortfolioImage]: A queryset containing cached portfolio images.
    """
    return get_cached_images("portfolio_images", PortfolioImage)


def handle_contact_form(request: HttpRequest, form: FeedbackForm, is_limited: bool) -> None:
    """
    Handles contact form submission.

    Args:
        request (HttpRequest): The incoming HTTP request.
        form (FeedbackForm): The feedback form instance.
        is_limited (bool): Whether the user is limited from sending requests.
    """
    if request.method == 'POST':
        if is_limited:
            messages.error(
                request, _("You are sending requests too often. Please wait 10 minutes.")
            )
        elif form.is_valid():
            try:
                data: Dict[str, Any] = form.cleaned_data
                send_email.delay(data)  # Асинхронная отправка email
                form.save()
                messages.success(request, _("Thank you\nI'll answer you very soon!"))
            except Exception as e:
                messages.error(request, _("An error occurred while processing your request."))
                print(f"Error processing contact form: {e}")  # Логирование ошибки

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
