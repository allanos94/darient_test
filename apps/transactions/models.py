from django.db import models

from apps.users.models import Client
from apps.utils.models import BaseModel


class ErrorCodeChoices(models.IntegerChoices):
    """
    Represents the error codes for a transaction.

    The error codes are:
    - 1: Invalid frontside image.
    - 2: Invalid backside image.
    - 3: Invalid frontside and backside images.
    - 4: Invalid client.
    - 5: Invalid frontside image and client.
    - 6: Invalid backside image and client.
    - 7: Invalid frontside and backside images and client.
    """

    INVALID_FRONTSIDE_IMAGE = 1
    INVALID_BACKSIDE_IMAGE = 2
    INVALID_FRONTSIDE_AND_BACKSIDE_IMAGES = 3
    INVALID_CLIENT = 4
    INVALID_FRONTSIDE_IMAGE_AND_CLIENT = 5
    INVALID_BACKSIDE_IMAGE_AND_CLIENT = 6
    INVALID_FRONTSIDE_AND_BACKSIDE_IMAGES_AND_CLIENT = 7


class Transaction(BaseModel):
    """
    Represents a transaction in the system.

    Inherits common fields and methods from the `BaseModel` class such as `created_at`, `updated_at`, `deleted_at`,
    and `is_active`.Defines additional fields specific to a transaction, such as the client, frontside and backside
    images, result, error code, and details.
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name="transactions")
    frontside_image = models.ImageField(upload_to="images/frontside_images", max_length=500)
    backside_image = models.ImageField(upload_to="images/backside_images", max_length=500)
    result = models.BooleanField(default=False)
    error_code = models.PositiveSmallIntegerField(blank=True, null=True, choices=ErrorCodeChoices.choices)
    details = models.CharField(blank=True, null=True, max_length=500)

    class Meta:
        db_table = "transactions"

    def __str__(self):
        """
        Returns a string representation of the transaction.

        Format: "{client} - status: {result}"
        """
        return f"{self.client} - status: {self.result}"
