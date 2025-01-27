from django.contrib import admin
from .models import MainImages
from django.conf import settings
from django.utils.html import format_html


@admin.register(MainImages)
class MainImagesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text', 'image')
    actions = ['swap_image']

    @admin.action(description="Swap selected images")
    def swap_image(self, request, queryset):
        """
        Swaps the images of exactly two selected MainImages objects.

        Args:
            request: The HTTP request object.
            queryset: A QuerySet containing the selected objects.

        Returns:
            None. Displays a success or error message to the user.
        """
        # Check if exactly two images are selected
        if queryset.count() != 2:
            self.message_user(
                request,
                "Please select exactly 2 images to swap.",
                level="error"
            )
            return

        # Retrieve the two selected objects
        image_1, image_2 = queryset

        # Swap their images
        image_1.image, image_2.image = image_2.image, image_1.image

        # Save changes to the database
        image_1.save()
        image_2.save()

        # Notify the user of success
        self.message_user(request, "Images swapped successfully.")


