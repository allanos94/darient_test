from drf_extra_fields.fields import HybridImageField
from rest_framework import serializers

from apps.transactions.models import Transaction
from apps.transactions.serializers_utils import decode_base64, format_errors, select_error_code, validate_image
from apps.users.models import Client


class TransactionReadSerializer(serializers.ModelSerializer):
    """
    A serializer for reading transaction data.

    Example Usage:
    ```python
    # Create an instance of TransactionReadSerializer
    serializer = TransactionReadSerializer(data=data)
    # Validate the data
    if serializer.is_valid():
        # Perform some action with the validated data
        ...
    ```

    Inputs:
    - data: The data to be serialized and validated.

    Outputs:
    - An instance of TransactionReadSerializer that can be used to serialize and validate transaction data.
    """

    class Meta:
        model = Transaction
        fields = (
            "id",
            "client",
            "result",
            "created_at",
            "error_code",
            "details",
        )


class ValidateSerializer(serializers.ModelSerializer):
    """
    A serializer for validating transaction data.

    Inputs:
    - client: The client field.
    - frontside_image: The frontside_image field.
    - backside_image: The backside_image field.

    Outputs:
    - An instance of ValidateSerializer that can be used to validate transaction data.
    """

    client = serializers.CharField()
    frontside_image = HybridImageField()
    backside_image = HybridImageField()

    def validate_client(self, value):
        """
        Validates the client.

        Inputs:
        - value: The client value to be validated.

        Outputs:
        - The validated client value.

        Raises:
        - serializers.ValidationError: If the client is invalid.
        """
        try:
            client = Client.objects.get(id=value)
        except Client.DoesNotExist:
            raise serializers.ValidationError({"error_detail": "Invalid client"})
        return client

    def validate_frontside_image(self, value):
        """
        Validates the frontside image.

        Inputs:
        - value: The frontside image value to be validated.

        Outputs:
        - The validated frontside image value.
        """
        return validate_image(value)

    def validate_backside_image(self, value):
        """
        Validates the backside image.

        Inputs:
        - value: The backside image value to be validated.

        Outputs:
        - The validated backside image value.
        """
        return validate_image(value)

    def create(self, validated_data):
        """
        Creates a transaction.

        Inputs:
        - validated_data: The validated transaction data.

        Outputs:
        - The created transaction instance.
        """
        validated_data["result"] = True
        return Transaction.objects.create(**validated_data)

    def failed(self, details, data):
        """
        Fails a transaction.

        Inputs:
        - details: The details of the failed transaction.
        - data: The transaction data.

        Outputs:
        - The created failed transaction instance.
        """
        client = Client.objects.filter(id=data["client"]).first()
        format_detail = format_errors(error_dict=details)
        if isinstance(data["frontside_image"], str):
            data["frontside_image"] = decode_base64(data["frontside_image"])
        if isinstance(data["backside_image"], str):
            data["backside_image"] = decode_base64(data["backside_image"])
        invalidated_data = {
            "client_id": client.id if client else None,
            "frontside_image": data["frontside_image"],
            "backside_image": data["backside_image"],
            "result": False,
            "error_code": select_error_code(details),
            "details": format_detail,
        }
        return Transaction.objects.create(**invalidated_data)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "client",
            "frontside_image",
            "backside_image",
            "result",
            "error_code",
            "details",
        )
