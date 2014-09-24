#coding: utf-8

from abc import ABCMeta, abstractmethod

class EntityUIProxyInterface(object):
    """
    Интерфейс для класса посредника между сущностями и UI
    """

    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def get_entities(cls):
        """
        Возвращает сущности для запроса
        """

    @classmethod
    @abstractmethod
    def get_entity_fields(cls, id):
        """
        возвращает поля сущности
        """

    @classmethod
    @abstractmethod
    def get_entities_fields(cls, ids):
        """
        Возвращает поля сущностей
        """
