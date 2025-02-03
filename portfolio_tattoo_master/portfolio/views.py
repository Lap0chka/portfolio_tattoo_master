from typing import Dict, Any, List, Tuple

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from pip._vendor.rich.markup import Tag

from django.conf import settings
from .form import FeedbackForm
from .models import Tag
from .utils import get_images, get_portfolio_images, handle_contact_form


@ratelimit(key='ip', rate='2/10m', method='POST', block=False)
def index(request: HttpRequest) -> HttpResponse:
    """
    Handles the main index page, including form submission and rate limiting.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered response with the context.
    """
    images = get_images()
    is_limited: bool = getattr(request, 'limited', False)

    form = FeedbackForm(request.POST or None)

    handle_contact_form(request, form, is_limited)

    context: Dict[str, Any] = {
        'images': images,
        'form': form,
        'is_limited': is_limited,
    }

    return render(request, 'portfolio/pages/index.html', context)


def refresh_captcha(request: HttpRequest) -> JsonResponse:
    """
    Refreshes the captcha and returns a new captcha image URL.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the new captcha key and image URL.
    """
    try:
        new_key: str = CaptchaStore.generate_key()
        new_image_url: str = captcha_image_url(new_key)
        return JsonResponse({'key': new_key, 'image_url': new_image_url})
    except Exception as e:
        print(f"Error generating captcha: {e}")  # Replace with logging in production
        return JsonResponse({'error': 'Failed to generate captcha'}, status=500)


def about_me(request: HttpRequest) -> HttpResponse:
    """
    Renders the 'About Me' page with images and their associated comments.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'about-me' template with context data.
    """
    images = get_images()
    comments: List[Tuple[str, str]] = [(image.text, image.author) for image in images if
                                       image.text and image.author]
    context = {
        'comments': comments,
    }
    return render(request, 'portfolio/pages/about-me.html', context)


def portfolio(request: HttpRequest) -> HttpResponse:
    """
    Renders the portfolio page with images and tags.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered portfolio page with context data.
    """
    portfolio_photos = get_portfolio_images()  # Исправлено имя переменной для консистентности
    tags = Tag.objects.all()

    context: Dict[str, Any] = {
        'portfolio_photos': portfolio_photos,
        'tags': tags,
    }

    return render(request, 'portfolio/pages/portfolio.html', context)


def information(request: HttpRequest) -> HttpResponse:
    """
    Renders the information page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered information page.
    """
    return render(request, 'portfolio/pages/information.html')


@ratelimit(key='ip', rate='2/10m', method='POST', block=False)
def contact(request: HttpRequest) -> HttpResponse:
    """
    Handles the contact page, including form submission and rate limiting.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered contact page.
    """
    is_limited: bool = getattr(request, 'limited', False)
    form = FeedbackForm(request.POST or None)

    handle_contact_form(request, form, is_limited)

    context: Dict[str, Any] = {
        'form': form,
        'is_limited': is_limited,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }

    return render(request, 'portfolio/pages/contact.html', context)
