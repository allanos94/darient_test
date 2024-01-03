import base64
import imghdr

from django.core.files.base import ContentFile
from rest_framework import serializers

IMAGE_VALID_FORMATS = ("jpeg", "jpg", "png", "bpm")


def validate_image(image):
    """
    Validates the image.

    Args:
        image (str or PIL.Image.Image): The image to be validated.

    Raises:
        serializers.ValidationError: If the image is invalid.

    Returns:
        PIL.Image.Image: The validated image.
    """
    if isinstance(image, str):
        try:
            image = decode_base64(image)
        except Exception as e:
            raise serializers.ValidationError({"error_detail": f"Invalid image, {e}"})
    img_format = imghdr.what(image)
    if img_format not in IMAGE_VALID_FORMATS:
        raise serializers.ValidationError({"error_detail": f"Invalid image format, must be {IMAGE_VALID_FORMATS}"})
    if image.image.width < 224 or image.image.height < 224:
        raise serializers.ValidationError({"error_detail": "Image too small, must be at least 224x224"})
    if image.image.width > 3840 or image.image.height > 2160:
        raise serializers.ValidationError({"error_detail": "Image too large, must be at most 3840x2160"})
    if image.size > 4 * 1024 * 1024:
        raise serializers.ValidationError({"error_detail": "Image too large, must be at most 4MB"})
    return image


def decode_base64(data):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


def select_error_code(details):
    """
    Selects the error code based on the details.

    Args:
        details (dict): The details of the error.

    Returns:
        int: The error code.
    """
    error_code = 0
    if details.get("frontside_image") and details.get("backside_image") and details.get("client"):
        error_code = 7
    elif details.get("frontside_image") and details.get("client"):
        error_code = 5
    elif details.get("backside_image") and details.get("client"):
        error_code = 6
    elif details.get("client"):
        error_code = 4
    elif details.get("frontside_image") and details.get("backside_image"):
        error_code = 3
    elif details.get("frontside_image"):
        error_code = 1
    elif details.get("backside_image"):
        error_code = 2
    return error_code


def format_errors(error_dict):
    """
    Formats the error dictionary into a string.

    Args:
        error_dict (dict): The error dictionary.

    Returns:
        str: The formatted error string.
    """
    result = ""
    for key, value in error_dict.items():
        error_detail = value.get('error_detail')
        if error_detail:
            result += f"{key}: {error_detail.__str__()}, "
    return result.rstrip(', ')
