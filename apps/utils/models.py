from django.db import models
from django.utils import timezone

from apps.users.managers import UserAccountManager


class SoftDeleteManager(UserAccountManager):
    """
    A custom manager class in Django that extends the UserManager class.
    Provides functionality for soft deleting records by filtering out records with a non-null deleted_at field.

    Example Usage:

    class MyModel(models.Model):
        objects = SoftDeleteManager()

        # Other fields and methods...

    # Soft delete a record
    my_record = MyModel.objects.get(id=1)
    my_record.delete()

    # Retrieve all records, including soft deleted ones
    all_records = MyModel.objects_with_deleted.all()

    # Retrieve only non-deleted records
    non_deleted_records = MyModel.objects.all()
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the SoftDeleteManager class and sets the with_deleted attribute based on the deleted keyword
        argument.

        Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Keyword Args:
        deleted (bool): Determines whether to include soft deleted records in the queryset. Defaults to False.
        """
        self.with_deleted = kwargs.pop("deleted", False)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)  # pylint: disable=super-with-arguments

    def _base_queryset(self):
        """
        Returns the base queryset by calling the get_queryset method of the parent UserManager class.

        Returns:
        QuerySet: The base queryset.
        """
        return super().get_queryset().all()

    def get_queryset(self):
        """
        Returns the queryset based on the with_deleted attribute.
        If with_deleted is True, it returns all records.
        If with_deleted is False, it filters out records with a non-null deleted_at field.

        Returns:
        QuerySet: The filtered queryset.
        """
        qs = self._base_queryset()
        if self.with_deleted:
            return qs
        return qs.filter(deleted_at=None)


class BaseModel(models.Model):
    """
    Base model for all models.

    This class provides common fields and methods for all models in the Django project.
    It includes fields such as 'created_at', 'updated_at', 'deleted_at', and 'is_active',
    and methods for saving and updating instances of the model.

    Fields:
    - created_at: A DateTimeField that automatically sets the value to the current date
                    and time when an instance is created.
    - updated_at: A DateTimeField that automatically updates the value to the current date and
                    time when an instance is updated.
    - deleted_at: A DateTimeField that stores the date and time when an instance is deleted.
                    If the instance is not deleted, the value is set to None.
    - is_active: A BooleanField that indicates whether an instance is active or not.
                    If an instance is not active, it is considered deleted and the 'deleted_at' field is set.

    Methods:
    - save(): Overrides the default save method to set the 'deleted_at' field if the instance is not active.
    - update(): A custom method that calls the save method to update an instance of the model.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        """
        Meta class for BaseModel

        Abstract is True because this model is not a table in the database, is a base for other models.
        """

        abstract = True

    objects = SoftDeleteManager()
    objects_with_deleted = SoftDeleteManager(deleted=True)

    def delete(self, *args, **kwargs):
        """
        Overrides the default delete method to set the 'deleted_at' field to the current date and time.
        """
        self.deleted_at = timezone.now()
        self.save()
