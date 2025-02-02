from typing import Dict, Union, List, Any, Tuple
from unittest.mock import patch

from captcha.models import CaptchaStore
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Model
from django.test import TestCase, override_settings
from django.urls import reverse

from portfolio.models import MainImages, Feedback
from .utils import get_images


class BaseViewTest(TestCase):
    """
     Base test case for testing views in the application.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating test images and test data.
        """
        self.image = MainImages.objects.create(image='image.jpg', text="Nice photo", author="John Doe")
        self.image2 = MainImages.objects.create(image='image.jpg', text="Great shot!", author="Jane Doe")
        self.image3 = MainImages.objects.create(image='image.jpg', text="", author="")
        self.url = reverse('index')
        self.data: Dict[str, str] = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello!',
        }
        cache.clear()

    def correct_content_render_to_template(self,
                                           url_name: str,
                                           template_name: str,
                                           member: str,
                                           expect: Union[Model, List[Any]],
                                           ) -> None:
        """
        Ensures that the correct template is used and the expected content is present in the context.

        Args:
            url_name (str): The URL name to reverse.
            template_name (str): The expected template name.
            member (str): The context key that should be present in the response.
            expect (Union[Model, List[Any]]): The expected object or list of objects
            (a Django model instance or a list of model instances).
        """
        response = self.client.get(reverse(url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertIn(member, response.context)
        context = response.context[member]
        self.assertQuerySetEqual(context, expect)

    @staticmethod
    def generate_captcha() -> Dict[str, str]:
        """
        Generates a valid captcha for form submission.

        Returns:
            Dict[str, str]: Captcha keys and values.
        """
        captcha_key = CaptchaStore.generate_key()
        captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
        return {'captcha_0': captcha_key, 'captcha_1': captcha_value}


class IndexViewTests(BaseViewTest):
    """
    Test case for the index view and related functionalities.
    """
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
        self.correct_content_render_to_template(
            'index',
            'portfolio/pages/index.html',
            'images',
            MainImages.objects.all(),
        )



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


class AboutMeViewTests(BaseViewTest):
    """
    Test cases for the About Me page view.
    """

    def test_about_me_renders_context_correct_template(self) -> None:
        """
        Tests that the About Me page renders the correct template
        and contains the expected comments in the context.
        """
        expected_comments: List[Tuple[str, str]] = [("Nice photo", "John Doe"), ("Great shot!", "Jane Doe")]

        self.correct_content_render_to_template(
            url_name='about',
            template_name='portfolio/pages/about-me.html',
            member='comments',
            expect=expected_comments
        )

    @patch('portfolio.views.get_images')
    def test_about_me_handles_empty_images_list(self, mock_get_images) -> None:
        """
        Tests that the About Me page correctly handles an empty image list.

        Args:
            mock_get_images (MagicMock): Mocked version of get_images function.
        """
        mock_get_images.return_value = []
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('comments', None), [])
