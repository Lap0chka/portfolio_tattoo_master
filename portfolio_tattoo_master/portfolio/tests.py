from typing import List, Any, Tuple
from unittest.mock import patch

from django.http.response import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import activate
from portfolio.models import MainImage


class BaseViewTest(TestCase):
    """
    Base test case for view-related assertions.
    """

    def assert_template_response_ok(self, response: HttpResponse, template_path: str) -> None:
        """
        Assert that the response has a 200 status code and uses the specified template.

        :param response: The HTTP response object to check.
        :param template_path: The expected template path.
        :return: None
        """
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_path)

    def assert_information_page_has_no_context(self, response: HttpResponse) -> None:
        """
        Assert that the rendered page does not contain a context dictionary.

        :param response: The HTTP response object to check.
        :return: None
        """
        self.assertFalse(response.context)

    def assert_information_page_contains_expected_text(self,
                                                       response: HttpResponse,
                                                       text1: str,
                                                       text2: str) -> None:
        """
        Assert that the information en page contains specific words.
        """
        self.assertContains(response, text1)
        self.assertContains(response, text2)

    def assert_switch_language(self, url):
        activate('de')
        response = self.client.get(url)
        self.assertEqual(get_language(), 'de')


class ImageTest(BaseViewTest):
    def setUp(self):
        """
            Set up the test environment by creating test images.
        """
        self.image = MainImage.objects.create(image='image.jpg', text="Nice photo",
                                              author="John Doe")
        self.image2 = MainImage.objects.create(image='image.jpg', text="Great shot!",
                                               author="Jane Doe")
        self.image3 = MainImage.objects.create(image='image.jpg', text="", author="")

    def assert_model_in_context(self, response: HttpResponse, context_key: str,
                                expected: List[Any]):
        """
        Ensures that a given model or queryset is present in the response context.

        Args:
            response (Response): The response object from a view.
            context_key (str): The key under which the model is stored in the context.
            expected:  The expected list model instance.
        """
        self.assertIn(context_key, response.context)
        context_value = response.context[context_key]
        self.assertQuerySetEqual(context_value, expected)


class AboutMeViewTests(ImageTest):
    """
    Test cases for the About Me page view.
    """
    def setUp(self):
        super().setUp()
        self.url = reverse('about')
        self.template_path = 'portfolio/pages/about-me.html'
        self.context_key = 'comments'
        self.response = self.client.get(self.url)

    def test_template_response_ok(self):
        self.assert_template_response_ok(self.response, self.template_path)

    def test_switch_language_in_session(self):
        self.assert_switch_language(self.url)

    def test_information_page_en_contains_expected_text(self):
        text1 = 'What can I tell you about me?'
        text2 = 'My favourite style'
        self.assert_information_page_contains_expected_text(self.response, text1, text2)

    def test_information_page_de_contains_expected_text(self):
        text1 = 'What can I tell you about me?'
        text2 = 'My favourite style'
        print(self.url)
        # self.assert_information_page_en_contains_expected_text(self.response, text1, text2)

    def test_model_in_context(self) -> None:
        """
            Tests that the About Me page renders the correct template
            and contains the expected comments in the context.
        """
        expected_comments: List[Tuple[str, str]] = [("Nice photo", "John Doe"), ("Great shot!", "Jane Doe")]

        self.assert_model_in_context(self.response, self.context_key,
                                     expected_comments)


    @patch('portfolio.views.get_images')
    def test_about_me_handles_empty_images_list(self, mock_get_images) -> None:
        """
        Tests that the About Me page correctly handles an empty image list.

        Args:
            mock_get_images (MagicMock): Mocked version of get_images function.
        """
        with patch('portfolio.views.get_images', return_value=[]):
            response = self.client.get(self.url)

        self.assert_model_in_context(response, self.context_key, [])


class PortfolioViewTests(ImageTest):
    def setUp(self):
        super().setUp()
        self.url = reverse('portfolio')
        self.template_path = 'portfolio/pages/portfolio.html'
        self.context_portfolio = 'portfolio_photos'
        self.context_tag = 'tags'
        self.response = self.client.get(self.url)

# class BaseViewTest(TestCase):
#     """
#      Base test case for testing views in the application.
#     """
#
#     def setUp(self) -> None:
#         """
#         Set up the test environment by creating test images and test data.
#         """
#         self.image = MainImage.objects.create(image='image.jpg', text="Nice photo", author="John Doe")
#         self.image2 = MainImage.objects.create(image='image.jpg', text="Great shot!", author="Jane Doe")
#         self.image3 = MainImage.objects.create(image='image.jpg', text="", author="")
#         self.url = reverse('index')
#         self.data: Dict[str, str] = {
#             'name': 'John Doe',
#             'email': 'john@example.com',
#             'message': 'Hello!',
#         }
#         cache.clear()
#
#     def correct_content_render_to_template(self,
#                                            url_name: str,
#                                            template_name: str,
#                                            member: str = None,
#                                            expect: Union[Model, List[Any]] = None,
#                                            ) -> None:
#         """
#         Ensures that the correct template is used and the expected content is present in the context.
#
#         Args:
#             url_name (str): The URL name to reverse.
#             template_name (str): The expected template name.
#             member (str): The context key that should be present in the response.
#             expect (Union[Model, List[Any]]): The expected object or list of objects
#             (a Django model instance or a list of model instances).
#         """
#         response = self.client.get(reverse(url_name))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, template_name)
#         if member:
#             self.assertIn(member, response.context)
#             context = response.context[member]
#             self.assertQuerySetEqual(context, expect)
#
#     @staticmethod
#     def generate_captcha() -> Dict[str, str]:
#         """
#         Generates a valid captcha for form submission.
#
#         Returns:
#             Dict[str, str]: Captcha keys and values.
#         """
#         captcha_key = CaptchaStore.generate_key()
#         captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
#         return {'captcha_0': captcha_key, 'captcha_1': captcha_value}
#
#
# class FormTestView(BaseViewTest):
#     """
#         Form test case for testing views in the application.
#     """
#
#     def setUp(self):
#         super().setUp()
#         self.data: Dict[str, str] = {
#             'name': 'John Doe',
#             'email': 'john@example.com',
#             'message': 'Hello!',
#         }
#
#     def post_request_valid_form(self, url: str):
#         """
#           Test view renders the correct template and context.
#         """
#         valid_data = self.data | self.generate_captcha()
#         initial_count = Feedback.objects.count()
#         response = self.client.post(url, data=valid_data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Feedback.objects.count(), initial_count + 1)
#
#         messages_list = [msg.message for msg in messages.get_messages(response.wsgi_request)]
#         self.assertIn("Thank you\nI'll answer you very soon!", messages_list)
#
#     def post_request_invalid_form(self, url) -> None:
#         """
#         Test that an invalid form submission does not create a Feedback entry and returns errors.
#         """
#         invalid_data = {'name': '', 'email': 'invalid-email', 'message': ''}
#         initial_count = Feedback.objects.count()
#
#         response = self.client.post(url, data=invalid_data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Feedback.objects.count(), initial_count)
#         messages_list = [msg.message for msg in messages.get_messages(response.wsgi_request)]
#         self.assertIn("name: This field is required.", messages_list)
#         self.assertIn("email: Enter a valid email address.", messages_list)
#
#     def post_request_rate_limited(self, url) -> None:
#         """
#         Test that excessive form submissions trigger rate limiting.
#         """
#         initial_count = Feedback.objects.count()
#
#         # Send 3 valid requests within the allowed limit
#         for _ in range(3):
#             valid_data = self.data | self.generate_captcha()
#             self.client.post(url, data=valid_data)
#
#         # Send one more request that should be rate-limited
#         valid_data = self.data | self.generate_captcha()
#         response = self.client.post(url, data=valid_data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Feedback.objects.count(), initial_count + 2)
#
#         messages_list = [msg.message for msg in messages.get_messages(response.wsgi_request)]
#         self.assertIn("You are sending requests too often. Please wait 10 minutes.", messages_list)
#
#     def exception_handling_in_post(self, url) -> None:
#         """
#         Tests that an exception raised during email sending is properly handled.
#         """
#         valid_data = self.data | self.generate_captcha()
#         initial_count = Feedback.objects.count()
#
#         # Simulate an exception when calling send_email.delay()
#         with patch("portfolio.utils.send_email.delay", side_effect=Exception("Test Exception")):
#             response = self.client.post(url, data=valid_data, follow=True)
#
#         self.assertEqual(response.status_code, 200)
#
#         # Ensure that the Feedback object was not created due to the exception
#         self.assertEqual(Feedback.objects.count(), initial_count)
#
#         # Check that the expected error message was added to Django messages
#         messages_list = [msg.message for msg in messages.get_messages(response.wsgi_request)]
#         self.assertIn("An error occurred while processing your request.", messages_list)
#
#
# class IndexViewTests(FormTestView):
#     """
#     Test case for the index view and related functionalities.
#     """
#     def setUp(self):
#         super().setUp()
#         self.url = reverse('index')
#
#     def test_get_images_from_cache(self) -> None:
#         """
#         Test that images are retrieved from the cache and not queried again.
#         """
#         cache.set('main_images', MainImage.objects.all(), timeout=60 * 30)
#
#         with patch('portfolio.models.MainImage.objects.all') as mock_queryset:
#             images = get_images()
#             mock_queryset.assert_not_called()
#
#         self.assertEqual(list(images), list(MainImage.objects.all()))
#
#     def test_index_renders_correct_template(self) -> None:
#         """
#         Test that the index view renders the correct template and context.
#         """
#         self.correct_content_render_to_template(
#             'index',
#             'portfolio/pages/index.html',
#             'images',
#             MainImage.objects.all(),
#         )
#
#     def test_post_request_valid_form(self) -> None:
#         """
#         Test that a valid form submission creates a Feedback entry and shows a success message.
#         """
#         self.post_request_valid_form(self.url)
#
#     def test_post_request_invalid_form(self) -> None:
#         """
#         Test that index an invalid form submission does not create a Feedback entry and returns errors.
#         """
#         self.post_request_invalid_form(self.url)
#
#
#     @override_settings(RATELIMIT_ENABLE=True)
#     def test_post_request_rate_limited(self) -> None:
#         """
#         Test that excessive form submissions trigger rate limiting.
#         """
#         self.post_request_rate_limited(self.url)
#
#
#     def test_exception_handling_in_post(self) -> None:
#         """
#         Tests that an exception raised during email sending is properly handled.
#         """
#         self.exception_handling_in_post(self.url)
#
#

#
# class InformationViewTests(BaseViewTest):
#     """
#     Test cases for the Information page view.
#     """
#
#     def test_information_template(self) -> None:
#         """
#         Tests that the information page renders the correct template.
#         """
#         self.correct_content_render_to_template(
#             url_name='information',
#             template_name='portfolio/pages/information.html',
#         )
#
#
# class ContactViewTests(FormTestView):
#     """
#     Test case for the contact view and related functionalities.
#     """
#     def setUp(self):
#         super().setUp()
#         self.url = reverse('contact')
#
#     def test_index_renders_correct_template(self) -> None:
#         """
#         Test that the index view renders the correct template and context.
#         """
#         self.correct_content_render_to_template(
#             'contact',
#             'portfolio/pages/contact.html',
#         )
#
#     def test_post_request_valid_form(self) -> None:
#         """
#         Test that a valid form submission creates a Feedback entry and shows a success message.
#         """
#         self.post_request_valid_form(self.url)
#
#     def test_post_request_invalid_form(self) -> None:
#         """
#         Test that index an invalid form submission does not create a Feedback entry and returns errors.
#         """
#         self.post_request_invalid_form(self.url)
#
#
#     @override_settings(RATELIMIT_ENABLE=True)
#     def test_post_request_rate_limited(self) -> None:
#         """
#         Test that excessive form submissions trigger rate limiting.
#         """
#         self.post_request_rate_limited(self.url)
#
#
#     def test_exception_handling_in_post(self) -> None:
#         """
#         Tests that an exception raised during email sending is properly handled.
#         """
#         self.exception_handling_in_post(self.url)
