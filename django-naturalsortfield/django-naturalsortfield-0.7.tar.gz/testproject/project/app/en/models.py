from django.db import models

from naturalsortfield.en import NaturalSortFieldEn

class NaturalSortModelEn(models.Model):
    title = models.CharField(max_length=255)
    natural_title = NaturalSortFieldEn('title', max_length=255)