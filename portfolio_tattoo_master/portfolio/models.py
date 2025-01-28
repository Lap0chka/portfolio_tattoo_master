import os
from typing import Any
from django.core.exceptions import ValidationError
from django.db import models


class MainImages(models.Model):
    """
    Model representing images for the main page.
    """
    image = models.ImageField(
        upload_to='main_images',
        help_text="Image for the main page."
    )
    text = models.TextField(
        blank=True,
        null=True,
        help_text="Optional text associated with the image."
    )
    author = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Author of the image."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the image was created."
    )

    def save(self, *args: Any, validate_limit: bool = True, **kwargs: Any) -> None:
        """
        Overrides the save method to enforce a limit on the number of images.

        Args:
            validate_limit (bool): Whether to validate the maximum number of images.
                                   Defaults to True.

        Raises:
            ValidationError: If the maximum number of images is exceeded.
        """
        max_images = 15
        if validate_limit:
            current_count = MainImages.objects.count()
            if current_count >= max_images:
                raise ValidationError(
                    f'A maximum of {max_images} images are allowed on the main page.'
                )
        super().save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> None:
        """
        Deletes the associated file when the model instance is deleted.
        """
        if self.image:
            image_path = self.image.path
            if os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    # Log the error (replace with logging in production)
                    print(f"Error deleting image file {image_path}: {e}")

        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns the object's position in the queryset as a string.

        Returns:
            str: The position of the object in the queryset, or "Object not found" if not found.
        """
        ordered_ids = list(MainImages.objects.order_by('pk').values_list('pk', flat=True))
        try:
            index = ordered_ids.index(self.pk) + 1
            return str(index)
        except ValueError:
            return "Object not found"

    class Meta:
        verbose_name = "Main Page Image"
        verbose_name_plural = "Main Page Images"
        ordering = ['pk']
