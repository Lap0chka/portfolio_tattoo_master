from typing import Dict, Any

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib import messages
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

from .form import FeedbackForm
from .task import send_email
from .utils import get_images


@ratelimit(key='ip', rate='3/10m', method='POST', block=False)
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

    if request.method == 'POST':
        if is_limited:
            messages.error(request, "You are sending requests too often. Please wait 10 minutes.")
        elif form.is_valid():
            try:
                data: Dict[str, Any] = form.cleaned_data
                send_email.delay(data)
                form.save()
                messages.success(request, "I'll answer you very soon!")
            except Exception as e:
                messages.error(request, "An error occurred while processing your request.")
                print(f"Error in form submission: {e}")  # Replace with logging in production
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

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


def about_me(request):
    images = get_images()
    comments = [(image.text, image.author) for image in images]
    context = {
        'comments': comments,
        'images': images,
    }
    return render(request, 'portfolio/pages/about-me.html', context)


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

