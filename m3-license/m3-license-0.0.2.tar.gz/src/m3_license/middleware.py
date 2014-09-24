# coding: utf-8
"""
File: middleware.py
Author: Rinat F Sabitov
Description: m3 license middleware
"""

from m3_license.api import get_project_lic_data


class LicenseMiddleware(object):
    """Предназначение простое: докидывать в объект
    реквеста данные из лицензии.
    Ожидается, что в settings уже прописаны LIC_KEY_FILE и PUBLIC_KEY
    """

    def process_request(self, request):
        """Добавляем в request содержимое лицензии
        """
        request.license = get_project_lic_data()
