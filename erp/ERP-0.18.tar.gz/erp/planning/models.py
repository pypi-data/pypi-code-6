__author__ = 'cltanuki'
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from erp.enterprise.models import CorpUser, CorpUnit


# GLTYPES = (
#     ('Направление', '0'),
#     ('Проект', '1'),
#     ('Категория', '2')
# )


STATUS = (
    ('0', 'PLANNED'),
    ('1', 'ACTIVE'),
    ('2', 'BLOCKED'),
    ('3', 'DONE', ),
)


# Create your models here.
# class Category(models.Model):
#     TODO: Refactor unusable class
#     title = models.CharField(verbose_name='Название', max_length=20)
#     gltype = models.IntegerField(verbose_name='Тип', choices=GLTYPES)
#     groups = models.ManyToManyField(CorpUnit, verbose_name='Группы, имеющие доступ к категории')
#
#     def __str__(self):
#         return self.name


class Project(models.Model):
    title = models.CharField(verbose_name='Название проекта', max_length=20)
    desc = models.TextField(verbose_name='Описание проекта')
    owner = models.ForeignKey(CorpUser, related_name='owned_prjs', verbose_name='Владелец проекта', editable=False)
    responsible = models.ForeignKey(CorpUnit, related_name='prj_responsible_unit',
                                    verbose_name='Ответственнач за проект группа')
    performer = models.ForeignKey(CorpUser, related_name='prj_performer',
                                  verbose_name='Исполнитель проекта', blank=True, null=True)
    started_at = models.DateTimeField(verbose_name='Создана', blank=True, null=True, auto_now_add=True, editable=False)
    deadline = models.DateTimeField(verbose_name='Плановое окончание')
    done_at = models.DateTimeField(verbose_name='Выполнен', blank=True, null=True, editable=False)
    public = models.BooleanField(verbose_name='Открытый проект')
    users = models.ManyToManyField(CorpUser, related_name='prj_assigned_users')
    item_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="Type")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('prj_item', args=[str(self.id)])

    def can_manage(self, user):
        return user == self.author


class TaskRes(models.Model):
    task = models.ForeignKey('Task')
    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="Тип")
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="Link")
    item = generic.GenericForeignKey('item_type', 'item_id')

    def __str__(self):
        return self.task

    def can_manage(self, user):
        return user == self.task.owner or user == self.task.performer


class Task(models.Model):
    title = models.CharField(verbose_name='Название задачи', max_length=20)
    desc = models.TextField(verbose_name='Описание задачи')
    owner = models.ForeignKey(CorpUser, related_name='owned_tasks', verbose_name='Владелец задачи', editable=False)
    public = models.BooleanField(verbose_name='Закрытая задача', blank=True)
    task_in = models.ForeignKey('Task', related_name='before_task',
                                verbose_name='Задание, которое должно быть окончено', blank=True, null=True)
    task_out = models.ForeignKey('Task', related_name='after_task', verbose_name='Задание, которое будет начато',
                                 blank=True, null=True)
    responsible = models.ForeignKey(CorpUnit, related_name='task_responsible_unit',
                                    verbose_name='Ответственная за задачу группа', blank=True, null=True)
    performer = models.ForeignKey(CorpUser, related_name='task_performer',
                                  verbose_name='Исполнитель задачи', null=True, blank=True)
    started_at = models.DateTimeField(verbose_name='Создана', blank=True, null=True, auto_now_add=True, editable=False)
    deadline = models.DateTimeField(verbose_name='Плановое окончание')
    done_at = models.DateTimeField(verbose_name='Выполнен', blank=True, null=True, editable=False)
    status = models.IntegerField(verbose_name='Статус', choices=STATUS, blank=True, null=True)
    prj = models.ForeignKey(Project, related_name='task_prj_container', verbose_name='Проект',
                            blank=True, null=True)
    users = models.ManyToManyField(CorpUser, verbose_name='Участники', related_name='task_assigned_users',
                                   blank=True, null=True)
    res = generic.GenericRelation(TaskRes, related_name='assigned_res')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('task_item', args=[str(self.id)])

    def is_owner(self, user):
        return user == self.owner

    def is_performer(self, user):
        return user == self.performer


class TaskTemplate(models.Model):
    title = models.CharField(verbose_name='Название шаблона задачи', max_length=20)
    desc = models.TextField(verbose_name='Описание шаблона задачи')
    responsible = models.ForeignKey(CorpUnit, related_name='responsible_unit',
                                    verbose_name='Ответственная за задачу группа')
    item_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="Type")

    def __str__(self):
        return self.name


class ProjectTemplate(models.Model):
    title = models.CharField(verbose_name='Название', max_length=20)
    desc = models.TextField(verbose_name='Описание шаблона проекта')
    req_tasks = models.ManyToManyField(TaskTemplate, related_name='req_task_templates',
                                       verbose_name='Обязательные задачи', blank=True)
    opt_tasks = models.ManyToManyField(TaskTemplate, related_name='opt_task_templates',
                                       verbose_name='Опциональные задачи', blank=True, null=True)
    responsible = models.ForeignKey(CorpUnit, related_name='prj_tmpl_responsible_unit',
                                    verbose_name='Ответственная за проект группа')
    item_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="Type")

    def __str__(self):
        return self.name