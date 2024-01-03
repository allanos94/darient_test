from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from apps.users.models import Client

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "password", "is_active", "is_staff")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        del attrs["password"]
        return attrs


class ClientReadSerializer(serializers.ModelSerializer):
    """
    A serializer for reading client data.
    """

    class Meta:
        model = Client
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "created_at",
        )


class ClientWriteSerializer(serializers.ModelSerializer):
    """
    A serializer for writing client data.
    """

    class Meta:
        model = Client
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "created_at",
        )
