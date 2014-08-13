"""
An error should be raised when attempting to use this app in conjunction with
any other app#
"""

from django.core.management.base import LabelCommand


class Command(LabelCommand):

    def handle_label(self, label, **options):
        pass
