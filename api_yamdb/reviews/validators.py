import datetime
import re

from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_username(value):
    """Не разрешает имя 'me' при регистрации."""

    if value == 'me':
        raise ValidationError(
            ('Измените имя пользователя.'),
            params={'value': value},
        )

    if re.match(r'^[\\w.@+-]+\\z', value):
        raise serializers.ValidationError(
            'Недопустимые символы в username.'
        )


def validate_year(value):
    """Проверяет значение года для произведения."""

    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(
            'Произведение не может быть из будущего'
        )
