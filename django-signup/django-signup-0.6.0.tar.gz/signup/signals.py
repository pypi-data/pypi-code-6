import django.dispatch

user_signed_up = django.dispatch.Signal(providing_args=['user', 'request'])
user_activated = django.dispatch.Signal(providing_args=['user', 'request'])
