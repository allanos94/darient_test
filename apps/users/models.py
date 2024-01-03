from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.users.managers import UserAccountManager
from apps.utils.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserAccountManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"


class Client(BaseModel):
    """
    Represents a client in the system.

    Fields:
    - first_name (CharField): The client's first name.
    - last_name (CharField): The client's last name.
    - email (EmailField): The client's email address.
    - phone_number (CharField, optional): The client's phone number.

    Inherits common fields and methods from the `BaseModel` class, such as `created_at`, `updated_at`,
    `deleted_at`, and `is_active`.
    """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "clients"

    def __str__(self):
        """
        Returns a string representation of the client.
        """
        return f"{self.first_name} {self.last_name}"
