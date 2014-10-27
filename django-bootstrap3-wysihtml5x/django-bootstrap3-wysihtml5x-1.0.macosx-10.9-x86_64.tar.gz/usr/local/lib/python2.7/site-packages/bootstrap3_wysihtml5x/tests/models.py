#-*- coding: utf-8 -*-

from django.db import models

from bootstrap3_wysihtml5x.fields import Wysihtml5xTextField

class ModelTest(models.Model):
    first_text = models.TextField()
    second_text = Wysihtml5xTextField()
