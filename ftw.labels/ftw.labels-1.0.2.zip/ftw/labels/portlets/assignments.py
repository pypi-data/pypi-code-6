from ftw.labels.portlets.interfaces import ILabelJarPortlet
from ftw.labels.portlets.interfaces import ILabelingPortlet
from plone.app.portlets.portlets.base import Assignment
from zope.interface import implements


class LabelJarAssignment(Assignment):
    implements(ILabelJarPortlet)

    @property
    def title(self):
        return 'ftw.labels: Label Jar Portlet'


class LabelingAssignment(Assignment):
    implements(ILabelingPortlet)

    @property
    def title(self):
        return 'ftw.labels: Labeling Portlet'
