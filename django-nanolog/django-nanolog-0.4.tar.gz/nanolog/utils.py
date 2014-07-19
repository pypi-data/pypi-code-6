from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from nanolog.models import Nanolog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def nanolog(log_type, details, note=None, user=None, ip=None, log_object=None, request=None):
    """
    Write into Nanolog the received data.

    <log_type>  - string
    <details>   - string
    <note>      - string
    <user>      - user instance or None
    <ip>        - string
    <log_object>- string
    <request>   - request object

    """
    if not log_type or not details:
        return
    if not user and request:
        user = request.user
    values = dict(
                user=user,
                log_type=log_type,
                details=details,
                note=note,
        )
    print(ip)
    if not ip and request:
        ip = get_client_ip(request)
    print(ip)
    try:
        validate_ipv46_address(ip)
        values['ip'] = ip
    except (ValidationError, TypeError):
        values['ip'] = None
    if log_object and hasattr(log_object, 'pk'):
        values['content_object'] = log_object
    Nanolog.objects.create(**values)
