from OFS.SimpleItem import SimpleItem
from zope.interface import implementer
from zope import schema
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty
from z3c.form.object import registerFactoryAdapter

from collective.configviews.api import ConfigurableBaseView
from . import messageFactory as _


class ICalendar(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        description=u'',
        required=True,
    )

    name = schema.TextLine(
        title=_(u'Name'),
        description=_(
            u'Used as unique identifier for a group of events. '
            u'It could be used as css class to change events style'
        ),
        required=True,
    )

    url = schema.TextLine(
        title=_(u'URL'),
        description=u'',
        required=True,
    )

    active = schema.Bool(
        title=_(u'Active'),
        description=u'',
        required=True,
        default=True
    )


@implementer(ICalendar)
class Calendar(SimpleItem):

    title = FieldProperty(ICalendar['title'])
    name = FieldProperty(ICalendar['name'])
    url = FieldProperty(ICalendar['url'])
    active = FieldProperty(ICalendar['active'])

    __name__ = ''
    __parent__ = None

    def getId(self):
        return self.__name__ or ''

    def to_dict(self):
        return {
            'title': self.title,
            'name': self.name,
            'url': self.url,
            'active': self.active,
        }

registerFactoryAdapter(ICalendar, Calendar)


class ICalendarView(Interface):

    calendars = schema.List(
        title=u'Calendars',
        description=u'',
        value_type=schema.Object(
            title=u"Calendar",
            schema=ICalendar
        ),
        required=True,
    )


class CalendarView(ConfigurableBaseView):
    settings_schema = ICalendarView

    def _format_cal(self, cal):
        cal = cal.to_dict().copy()
        css_class = '{0} badge'.format(cal['name'])
        if not cal['active']:
            css_class += ' calendar-unchecked'
        cal['css_class'] = css_class
        return cal

    def calendars(self):
        if self.settings['calendars']:
            return [self._format_cal(i) for i in self.settings['calendars']]
