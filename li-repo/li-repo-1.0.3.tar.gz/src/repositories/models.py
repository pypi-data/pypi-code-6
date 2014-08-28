# -*- coding: utf-8 -*-
from django.db import models


class Pais(models.Model):
    """Países."""
    id = models.CharField(db_column="pais_id", max_length=3, primary_key=True)
    nome = models.CharField(db_column="pais_nome", max_length=64)
    numero = models.CharField(db_column="pais_numero", max_length=3)
    codigo = models.CharField(db_column="pais_codigo", max_length=2, unique=True)

    class Meta:
        app_label = "domain"
        db_table = u"tb_pais"
        verbose_name = u"País"
        verbose_name_plural = u"Países"
        ordering = ["nome"]

    def __unicode__(self):
        return self.nome
