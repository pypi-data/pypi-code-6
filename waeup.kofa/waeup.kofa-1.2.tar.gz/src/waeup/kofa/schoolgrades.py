## $Id: schoolgrades.py 9055 2012-07-26 06:32:08Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Components representing and aggregating school grades.
"""
import grok
from zope.formlib.interfaces import IInputWidget, IDisplayWidget
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.fieldproperty import FieldProperty
from zope.schema import Object
from waeup.kofa.interfaces import IResultEntry, IResultEntryField
from waeup.kofa.widgets.objectwidget import (
    KofaObjectWidget, KofaObjectDisplayWidget
    )

class ResultEntry(grok.Model):
    """A result entry contains a subject and a grade.
    """
    grok.implements(IResultEntry)
    subject = FieldProperty(IResultEntry['subject'])
    grade = FieldProperty(IResultEntry['grade'])

    def __init__(self, subject=None, grade=None):
        super(ResultEntry, self).__init__()
        if subject is not None:
            self.subject = subject
        if grade is not None:
            self.grade = grade
        return

    def to_string(self):
        """A string representation that can be used in exports.

        Returned is a unicode string of format ``(u'<SUBJ>',u'<GRADE>')``.
        """
        return unicode((self.subject, self.grade))

    @classmethod
    def from_string(cls, string):
        """Create new ResultEntry instance based on `string`.

        The string is expected to be in format as delivered by
        meth:`to_string`.

        This is a classmethod. This means, you normally will call::

          ResultEntry.from_string(mystring)

        i.e. use the `ResultEntry` class, not an instance thereof.
        """
        string = string.replace("u''", "None")
        subject, grade = eval(string)
        return cls(subject, grade)

class ResultEntryField(Object):
    """A zope.schema-like field for usage in interfaces.

    If you want to define an interface containing result entries, you
    can do so like this::

      class IMyInterface(Interface):
          my_result_entry = ResultEntryField()

    Default widgets are registered to render result entry fields.
    """
    grok.implements(IResultEntryField)

    def __init__(self, **kw):
        super(ResultEntryField, self).__init__(IResultEntry, **kw)
        return

# register KofaObjectWidgets as default widgets for IResultEntryFields
@grok.adapter(IResultEntryField, IBrowserRequest)
@grok.implementer(IInputWidget)
def result_entry_input_widget(obj, req):
    return KofaObjectWidget(obj, req, ResultEntry)

# register a display widget for IResultEntryFields
@grok.adapter(IResultEntryField, IBrowserRequest)
@grok.implementer(IDisplayWidget)
def result_entry_display_widget(obj, req):
    return KofaObjectDisplayWidget(obj, req, ResultEntry)
