#coding: utf-8

from abc import ABCMeta, abstractmethod

class ReportComponentOneToOneProxy(object):
    """
    Набор методов для работы со связанными с Report моделями(имеющих связь 1:1)
    """

    __metaclass__ = ABCMeta

    # Указывается в потомках
    model_cls = None

    @classmethod
    def _get_or_create(cls, report):

        assert cls.model_cls

        try:
            instance = cls.model_cls.objects.get(report=report)
        except cls.model_cls.DoesNotExist:
            instance = cls.model_cls(report=report)

        return instance

    @classmethod
    @abstractmethod
    def _prepare_instance(cls, report, instance, *args):
        """
        """

    @classmethod
    def save(cls, report, *args):
        """
        получение и сохранение экземпляра
        """
        instance = cls._get_or_create(report)
        instance = cls._prepare_instance(report, instance, *args)

        instance.save()


class ReportComponentManyToOneProxy(object):
    """
    Набор методов для работы со связанными с Report моделями(имеющих связь m:1)
    """

    __metaclass__ = ABCMeta

    model_cls = None

    @classmethod
    def _clean(cls, report):

        assert cls.model_cls

        cls.model_cls.objects.filter(report=report).delete()

    @classmethod
    @abstractmethod
    def _prepare_instance(cls, report, instance, param):
        """
        """

    @classmethod
    def save(cls, report, params):
        """
        Создание экземпляров связанных моделей
        """
        cls._clean(report)

        for param in params:
            instance = cls.model_cls(report=report)
            instance = cls._prepare_instance(report, instance, param)
            instance.save()
