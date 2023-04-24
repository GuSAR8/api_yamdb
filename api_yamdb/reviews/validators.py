from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_current_year(value):
    if value > timezone.localtime(timezone.now()).year:
        raise ValidationError('Год не превышает текущий.')
