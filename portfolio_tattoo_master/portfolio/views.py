from django.core.cache import cache
from django.shortcuts import render

from .models import MainImages


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


def index(request):
    """
    Handles the request for the index page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the index page with a list of images and a title.
    """
    # Fetch all images from the database
    images = get_images()

    # Prepare context for the template
    context = {
        'images': images,
        'title': 'Welcome',
    }

    # Render and return the response
    return render(request, 'portfolio/pages/index.html', context)


def about_me(request):
    return render(request, 'portfolio/pages/about-me.html', )


def portfolio(request):
    return render(request, 'portfolio/pages/portfolio.html',)


def information(request):
    return render(request, 'portfolio/pages/information.html', )


def contact(request):
    return render(request, 'portfolio/pages/contact.html', )


def blog(request):
    return render(request, 'portfolio/pages/blog.html', )


def post_deteil(request, post):
    return render(request, 'portfolio/pages/blog-about.html', )

