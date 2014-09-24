#coding: utf-8

import json

from django.db import models

import settings

from report_generator.constructor_settings import TEMPLATE_DIR

class SectionTypeOutput(object):
    """
    Тип вывода секции
    """

    # Горизонтальная развертка
    GORIZONTAL = u'Горизонтальный'

    # Вертикальная развертка
    VERTICAL = u'Вертикальная'

    VALUES = [GORIZONTAL, VERTICAL]


class Report(models.Model):
    """
    Модель отчета
    """

    # Идентификатор отчета
    report_key = models.CharField(max_length=50)

    # Название отчета
    name = models.CharField(max_length=100)

    def get_sections(self):
        """
        Возвращает декодированные секции
        """
        return self.template.get_sections()

    def get_template_name(self):
        """
        Возвращает имя шаблона
        """
        return self.template.get_template_name()

    def get_template_file(self):
        """
        Возвращаем файл шаблона
        """
        return self.template.get_file()

    def get_subst_values(self):
        """
        Значения для подстановки
        """
        return self.subst_values.get_subst_values()

    def get_document_type(self):
        return self.template.document_type

    class Meta:
        verbose_name = u'Отчет'
        verbose_name_plural = u'Отчеты'


class ReportQuery(models.Model):
    """
    Связь запроса и отчета
    """

    # Ссылка на запрос
    report = models.ForeignKey('Report', related_name='queries')

    # Идентификатор запроса
    query_id = models.IntegerField()


class Template(models.Model):
    """
    Шаблон отчета
    """

    # Название файла
    file_name = models.CharField(max_length=100)

    # Файл шаблона
    file = models.FileField(upload_to=TEMPLATE_DIR)

    # Тип документа
    document_type = models.IntegerField(default=-1)

    # Строковое представление JSON обьекта список секций
    # Для работы используется TemplateProxy
    json_sections = models.TextField()

    report = models.OneToOneField('Report', related_name='template')

    def get_sections(self):
        return json.loads(self.json_sections)

    def get_template_name(self):
        return self.file_name

    def get_file(self):
        return self.file

    def get_document_type(self):
        return self.document_type


class FormField(models.Model):
    """
    """

    report = models.ForeignKey('Report', related_name='form_fields')

    # Строковое представление полей, которые должны генерироваться на форме получения запросов
    json_fields = models.TextField()

    def get_fields(self):
        return json.loads(self.json_fields) if self.json_fields else {}

class SubstValues(models.Model):
    """
    """

    report = models.OneToOneField('Report', related_name='subst_values')

    json_subst_values =  models.TextField()

    def get_subst_values(self):
        return json.loads(self.json_subst_values) if self.json_subst_values else {}