#coding: utf-8

from django.utils import importlib
from django.conf import settings

from sqlalchemy.exc import OperationalError

from alchemy_wrapper import SQLAlchemyWrapper, AlchemyWrapperError

from report_generator.exceptions import ReportGeneratorError


class WrapperBuilder(object):
    """
    Построение wrapper-ов
    """

    @classmethod
    def build_wrapper(cls):
        """
        Возвращает враппер
        """
        settings_module = importlib.import_module(settings.SETTINGS_MODULE)

        try:
            return SQLAlchemyWrapper(settings_module.DATABASES)
        except (AlchemyWrapperError, OperationalError):
            raise ReportGeneratorError(u"Неверные настройки подключения к БД")

if (
    hasattr(settings, 'PREBUILD_ALCHEMY_WRAPPER') and
    settings.PREBUILD_ALCHEMY_WRAPPER
):
    WrapperBuilder.build_wrapper()