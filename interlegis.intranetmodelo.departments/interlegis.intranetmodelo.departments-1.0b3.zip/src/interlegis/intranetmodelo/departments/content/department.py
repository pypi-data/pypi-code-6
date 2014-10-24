# -*- coding: utf-8 -*-

from five import grok
from interlegis.intranetmodelo.departments.interfaces import IDepartment
from plone.dexterity.content import Container


class Department(Container):
    """Exemplo de tipo de conteúdo."""

    grok.implements(IDepartment)
