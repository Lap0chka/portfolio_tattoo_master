from .models import MainImages
from django.core.cache import cache

def get_images() -> 'QuerySet':
    """
    Retrieves all images from the cache or database.

    Returns:
        QuerySet: A queryset containing all images.
    """
    images = cache.get('all_images')
    if not images:
        images = MainImages.objects.all()
        cache.set('all_images', images, timeout=60 * 30)  # 30 minutes

    return images