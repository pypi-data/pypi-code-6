"""
.. _ics:

Send a calendar event
=====================

There are many different types of calendar events, distinguished by the 
method:

:PUBLISH_: when you just want to inform people of an event
:REQUEST_: when you require a response


example::

    info = dict(
       location='My location',
       dtstart=datetime(2008, 6, 2, 15, 30),
       dtend=datetime(2008, 6, 2, 24, 00),
       organizer=('adentella@thundersystems.it', 'Sandro Dentella')
    )
 
    msg = EmailMessageCalendar(title, summary, from_email, recipient_list)
    event = msg.get_event(info)
    msg.set_attendee(event, email2, full_name) # Required for ``REQUEST``
    msg.attach_calendar(event, 'PUBLISH')
    msg.send()
 

.. autoclass:: EmailMessageCalendar
   :members: get_event, attach_calendar, set_attendee, set_organizer


.. _PUBLISH: http://tools.ietf.org/html/rfc2446#section-3.2.1
.. _REQUEST: http://tools.ietf.org/html/rfc2446#section-3.2.2
"""


import uuid
import email
from email import MIMEText, MIMEBase
from email.MIMEMultipart import MIMEMultipart
import datetime as dt
import icalendar
import pytz 
 
from django.core.mail.message import EmailMessage

class EmailMessageCalendar(EmailMessage):
    """An EmailMessage capable of creating a correct Ics attachment
    
    
    """
    filename = "meeting.ics"
    # default properties for the event

    def set_organizer(self, event, email, full_name=None):
        """Set the organizer of the meeting

        :arg email: the email
        :arg full_name: the full name
        """
        
        organizer = icalendar.vCalAddress('MAILTO:%s' % email)
        organizer.params['cn'] = icalendar.vText(full_name)
        event['organizer'] = organizer

        
    def set_attendee(self, event, email, full_name=None):
        """Set an attendee of the meeting. Required if method is ``REQUEST``

        :arg email: the email
        :arg full_name: the full name
        """
        attendee = icalendar.vCalAddress('MAILTO:%s' % email)
        if full_name:
            attendee.params['cn'] = icalendar.vText(full_name)
        attendee.params['ROLE'] = icalendar.vText('REQ-PARTICIPANT')
        event.add('attendee', attendee, encode=0)

        
    def get_event(self, props=None, meth='PUBLISH'):
        """Return a basic event to be added to a calendar event.
        ``uuid`` and ``dtstamp`` are added by default if not present.
        ``attendee and `organizer`` can be eather email or tuple (email, common_name)
        and will be correctly adde using :meth:`set_organizer` and 
        meth:`set_attendee`.
        
        :arg props: a dict of properties to be added to the event.
           read rfc_ to get more info on usable params

        :arg meth: the method of the calendar that will be created. Default: ``PUBLISH``

        .. _rfc: http://tools.ietf.org/html/rfc2446#section-3.2.2

        """
        assert props or event, "An event or a dict of properties must be provided"
        tz = pytz.timezone("Europe/Rome")
        event = icalendar.Event()

        if not 'uuid' in props:
            props['uuid'] = uuid.uuid1().hex

        if not 'dtstamp' in props:
            props['dtstamp'] = tz.localize(dt.datetime.now())

        for key, value in props.iteritems():
            if key.lower() == 'organizer':
                if isinstance(value, basestring):
                    self.set_organizer(event, value)
                else:
                    self.set_organizer(event, value[0], value[1] if len(value) >1 else '')
            elif key.lower() == 'attendee':
                if isinstance(value, basestring):
                    self.set_attendee(event, value)
                else:
                    self.set_attendee(event, value[0], value[1:] if len(value) >1 else '')
            else:    
                event.add(key, value)

        return event

    def create_ics_attachment(self, cal):
        part = email.MIMEBase.MIMEBase('text', "calendar", method="REQUEST", name=self.filename)
        part.set_payload( cal.to_ical() )
        #email.Encoders.encode_base64(part)
        email.Encoders.encode_7or8bit(part)
        part.add_header('Content-Description', self.filename)
        part.add_header("Content-class", "urn:content-classes:calendarmessage")
        part.add_header("Filename", self.filename)
        part.add_header("Path", self.filename)
        return part


    def get_calendar(self, meth):
        """Return an icalendar.Calendar containing event
        You may wish to customize this to add alarms or other events

        :arg event: the icalendar.Event
        :arg meth: the method declared in the calendar. Defaults to 'PUBLISH', 
           You may prefere 'REQUEST' if you want a reply. It you use ``REQUEST``
           you must add attendee
        """
        cal = icalendar.Calendar()
        cal.add('prodid', '-//Jumbo framework//')
        cal.add('version', '2.0')
        cal.add('method', meth)
        return cal
    

    def attach_calendar(self, events, meth='PUBLISH', calendar=None):
        """
        Set a calendar 
        """
        calendar = calendar or self.get_calendar(meth)

        if not isinstance(events, (tuple, list, set)):
            events = [events]
        for event in events:
            calendar.add_component(event)

        part = self.create_ics_attachment(calendar)
        self.attach(part)
        
