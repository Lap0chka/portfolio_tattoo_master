import os
from typing import Any, Optional

from django.contrib import admin
from django.http import HttpRequest

from .models import MainImage, Feedback, PortfolioImage, Tag


@admin.register(MainImage)
class MainImagesAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for MainImages model.
    Includes custom actions for swapping images and deleting associated image files.
    """
    list_display = ('__str__', 'text', 'image')
    actions = ['swap_image']

    @admin.action(description="Swap selected images")
    def swap_image(self, request: HttpRequest, queryset: Any) -> None:
        """
        Swaps the images of exactly two selected MainImages objects.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (Any): A QuerySet containing the selected objects.

        Returns:
            None. Displays a success or error message to the user.
        """
        if queryset.count() != 2:
            self.message_user(
                request,
                "Please select exactly 2 images to swap.",
                level="error"
            )
            return

        # Retrieve the two selected objects
        image_1, image_2 = queryset

        try:
            # Swap their images
            image_1.image, image_2.image = image_2.image, image_1.image

            # Save changes to the database
            image_1.save()
            image_2.save()

            # Notify the user of success
            self.message_user(request, "Images swapped successfully.")
        except Exception as e:
            # Log and display an error message
            print(f"Error while swapping images: {e}")
            self.message_user(
                request,
                "An error occurred while swapping the images.",
                level="error"
            )

    def delete_queryset(self, request: HttpRequest, queryset: Any) -> None:
        """
        Deletes the selected queryset of objects and removes the associated image files.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (Any): The queryset of objects to be deleted.

        Returns:
            None: This method does not return anything, it only performs the deletion of objects and files.
        """
        for obj in queryset:
            if obj.image:
                try:
                    # Remove the associated image file
                    image_path = obj.image.path
                    if os.path.isfile(image_path):
                        os.remove(image_path)
                except Exception as e:
                    print(f"Error deleting file {image_path}: {e}")

        # Proceed with the default deletion of objects from the database
        super().delete_queryset(request, queryset)

    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        """
        Deletes a single object and removes the associated image file.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Any): The object to be deleted.

        Returns:
            None: This method does not return anything, it only performs the deletion of the object and file.
        """
        if obj.image:
            try:
                # Remove the associated image file
                image_path = obj.image.path
                if os.path.isfile(image_path):
                    os.remove(image_path)
            except Exception as e:
                print(f"Error deleting file {image_path}: {e}")

        # Proceed with the default deletion of the object from the database
        super().delete_model(request, obj)


@admin.register(Feedback)
class FeedBackAdmin(admin.ModelAdmin):
    """
    Admin configuration for Feedback model.
    """
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    """
    Admin configuration for Tag model.
    """
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(PortfolioImage)
class PortfolioPhotoAdmin(admin.ModelAdmin):
    """
    Admin configuration for PortfolioImage model.
    """
    list_display = ('id', 'uploaded_at', 'tag_list')
    list_filter = ('tags', 'uploaded_at')
    search_fields = ('tags__name',)
    filter_horizontal = ('tags',)

    def tag_list(self, obj: PortfolioImage) -> Optional[str]:
        """
        Returns a comma-separated list of tags associated with the PortfolioImage.

        Args:
            obj (PortfolioImage): The PortfolioImage instance.

        Returns:
            Optional[str]: A string representation of associated tags, or None if no tags exist.
        """
        tags = obj.tags.all()
        return ", ".join(tag.name for tag in tags) if tags.exists() else None

    tag_list.short_description = "Tags"

