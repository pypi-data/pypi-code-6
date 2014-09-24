# coding: utf-8
"""
File: license_status.py
Author: Rinat F Sabitov
Description:
"""

from django.core.management.base import BaseCommand
import sys


class Command(BaseCommand):
    """Простая проверка лицензии на валидность.
    Исходя из ее результатов будут приниматься
    решения об обновлении системы
    """

    def handle(self, *args, **options):
        from m3_license.api import get_project_lic_data, LicenseException
        try:
            get_project_lic_data()
        except LicenseException as err:
            sys.stderr.write(unicode(err))
            sys.exit(1)
        sys.exit(0)
