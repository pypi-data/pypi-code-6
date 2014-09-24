#coding: utf-8

from django.db import models

class Query(models.Model):
    """
    Модель запроса
    """

    # Имя запроса
    name = models.CharField(max_length=300)

    # Сериализованный JSON обьект представляющий запрос
    # Для работы с запросом используйте прокси класс QueryProxy
    json_query = models.TextField()