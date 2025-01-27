from django.shortcuts import render
from .models import MainImages



def index(request):
    """
    Handles the request for the index page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the index page with a list of images and a title.
    """
    # Fetch all images from the database
    images = MainImages.objects.all()

    # Prepare context for the template
    context = {
        'images': images,
        'title': 'Welcome',
    }
    for ind, image in enumerate(images, 1):
        print(f'{ind}. {image.image}')
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

