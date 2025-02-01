from typing import Dict
from unittest.mock import patch

from captcha.models import CaptchaStore
from django.contrib import messages
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from portfolio.models import MainImages, Feedback
from .utils import get_images



class IndexViewTests(TestCase):
    """
    Test case for the index view and related functionalities.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating test images and test data.
        """
        self.image = MainImages.objects.create(image='image.jpg')
        self.url = reverse('index')
        self.data: Dict[str, str] = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello!',
        }
        cache.clear()

    def generate_captcha(self) -> Dict[str, str]:
        """
        Generates a valid captcha for form submission.

        Returns:
            Dict[str, str]: Captcha keys and values.
        """
        captcha_key = CaptchaStore.generate_key()
        captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
        return {'captcha_0': captcha_key, 'captcha_1': captcha_value}

    def test_get_images_from_cache(self) -> None:
        """
        Test that images are retrieved from the cache and not queried again.
        """
        cache.set('all_images', MainImages.objects.all(), timeout=60 * 30)

        with patch('portfolio.models.MainImages.objects.all') as mock_queryset:
            images = get_images()
            mock_queryset.assert_not_called()

        self.assertEqual(list(images), list(MainImages.objects.all()))

    def test_index_renders_correct_template(self) -> None:
        """
        Test that the index view renders the correct template and context.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/pages/index.html')

        self.assertIn('images', response.context)
        images = response.context['images']
        self.assertQuerySetEqual(images, MainImages.objects.all(), transform=lambda x: x)

    def test_post_request_valid_form(self) -> None:
        """
        Test that a valid form submission creates a Feedback entry and shows a success message.
        """
        valid_data = self.data | self.generate_captcha()
        initial_count = Feedback.objects.count()

        response = self.client.post(self.url, data=valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), initial_count + 1)

        messages_list = [msg.message for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn("Thank you\nI'll answer you very soon!", messages_list)

    def test_post_request_invalid_form(self) -> None:
        """
        Test that an invalid form submission does not create a Feedback entry and returns errors.
        """
        invalid_data = {'name': '', 'email': 'invalid-email', 'message': ''}
        initial_count = Feedback.objects.count()

        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), initial_count)

        messages_list = [msg.message for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn("name: This field is required.", messages_list)
        self.assertIn("email: Enter a valid email address.", messages_list)

    @override_settings(RATELIMIT_ENABLE=True)
    def test_post_request_rate_limited(self) -> None:
        """
        Test that excessive form submissions trigger rate limiting.
        """
        initial_count = Feedback.objects.count()

        # Send 3 valid requests within the allowed limit
        for _ in range(3):
            valid_data = self.data | self.generate_captcha()
            self.client.post(self.url, data=valid_data)

        # Send one more request that should be rate-limited
        valid_data = self.data | self.generate_captcha()
        response = self.client.post(self.url, data=valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), initial_count + 3)

        messages_list = [msg.message for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn("You are sending requests too often. Please wait 10 minutes.", messages_list)

    def test_exception_handling_in_post(self) -> None:
        """
        Tests that an exception raised during email sending is properly handled.
        """
        valid_data = self.data | self.generate_captcha()
        initial_count = Feedback.objects.count()

        # Simulate an exception when calling send_email.delay()
        with patch("portfolio.views.send_email.delay", side_effect=Exception("Test Exception")):
            response = self.client.post(self.url, data=valid_data, follow=True)

        self.assertEqual(response.status_code, 200)

        # Ensure that the Feedback object was not created due to the exception
        self.assertEqual(Feedback.objects.count(), initial_count)

        # Check that the expected error message was added to Django messages
        messages_list = [msg.message for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn("An error occurred while processing your request.", messages_list)

