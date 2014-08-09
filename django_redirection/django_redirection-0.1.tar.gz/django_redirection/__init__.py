# -*- coding: utf-8 -*-

""" django_redirector  X-Accel-Redirect / X-Sendfile  application for django.

nginx and Apache has a backend redirection function named X-Accel-Rediect and X-Sendfile.
django_redirector auth user and redirect to other backends.
"""


from urls import generate_url
