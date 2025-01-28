from django.core.cache import cache
from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse

from portfolio.models import MainImages
from portfolio.views import get_images


class IndexViewTests(TestCase):
    """
    Test case for the index view and related functionalities.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating test images.
        """
        self.image1 = MainImages.objects.create(image="image1.jpg")
        self.image2 = MainImages.objects.create(image="image2.jpg")
        cache.clear()

    def test_get_images_from_cache(self) -> None:
        """
        Test that images are retrieved from the cache and not queried again.
        """
        # Set the cache with all images
        cache.set('all_images', MainImages.objects.all(), timeout=60 * 30)

        # Patch the MainImages queryset to ensure it is not called
        with patch('portfolio.views.MainImages.objects.all') as mock_queryset:
            images = get_images()
            mock_queryset.assert_not_called()

        # Verify that the retrieved images match the expected images
        self.assertEqual(list(images), list(MainImages.objects.all()))

    def test_index_renders_correct_template(self) -> None:
        """
        Test that the index view renders the correct template and context.
        """
        # Perform a GET request to the index URL
        url = reverse('index')
        response = self.client.get(url)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Verify the correct template is used
        self.assertTemplateUsed(response, 'portfolio/pages/index.html')

        # Verify the context contains the correct title
        title = response.context['title']
        self.assertEqual(title, 'Welcome')

        # Verify the context contains images and they match the database
        self.assertIn('images', response.context)
        images = response.context['images']
        self.assertQuerySetEqual(images, MainImages.objects.all(), transform=lambda x: x)
