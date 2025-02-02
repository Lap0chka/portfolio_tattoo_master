from typing import Type

from django.db.models import Model, QuerySet

from .models import MainImage, PortfolioImage
from django.core.cache import cache


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