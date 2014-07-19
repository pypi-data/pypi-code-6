from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from nanolog.models import Nanolog


def nanolog(log_type, details, note=None, user=None, ip=None, log_object=None):
    """
    Write into Nanolog the received data.

    <log_type>  - string
    <details>   - string
    <note>      - string
    <user>      - user instance or None
    <ip>        - string
    <log_object>    - string
    """
    if not log_type or not details:
        return
    values = dict(
                user=user,
                log_type=log_type,
                details=details,
                note=note,
                ip=ip,
        )
    try:
        validate_ipv46_address(ip)
    except (ValidationError, TypeError):
        values['ip'] = None
    if log_object and hasattr(log_object, 'pk'):
        values['content_object'] = log_object
    Nanolog.objects.create(**values)
