import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(username):
    regex = re.compile(r'^[\w.@+-]+\Z', re.I)
    match = regex.match(str(username))
    if match and username.lower() != 'me':
        return username
    raise ValidationError(
        ('Недоступное имя пользователя.'),
        params={'value': username},
    )


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError(
            'Нельзя указывать произведения из будущего!',
        )
    return year
