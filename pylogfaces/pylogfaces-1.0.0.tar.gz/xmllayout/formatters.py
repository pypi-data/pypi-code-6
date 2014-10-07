"""logging Formatters"""

__author__    = 'Philip Jenvey <pjenvey@groovie.org>, Stojan Jovic <stojan.jovic@dmsgroup.rs>'
__contact__   = 'pjenvey@groovie.org, stojan.jovic@dmsgroup.rs'
__date__      = '19 August 2007'
__copyright__ = 'Python Software Foundation'

# Modified: 29 January 2009
import cgi
import logging

__all__ = ['XMLLayout']

class XMLLayout(logging.Formatter):
    """Formats log Records as XML according to the `log4j XMLLayout
    <http://logging.apache.org/log4j/docs/api/org/apache/log4j/xml/
    XMLLayout.html>_`
    """
    
    def __init__(self, properties=None):
        logging.Formatter.__init__(self)
        
        self.properties = properties

    def format(self, record):
        """Format the log record as XMLLayout XML"""
        levelname = record.levelname
        if levelname == 'VERBOSE':
            levelname = 'TRACE'
        elif levelname == 'WARNING':
            levelname = 'WARN'
        elif levelname == 'CRITICAL':
            levelname = 'FATAL'
        event = dict(name=cgi.escape(record.name),
                     threadName=cgi.escape(record.threadName),
                     levelname=cgi.escape(levelname),
                     created=int(record.created * 1000))

        event['message'] = LOG4J_MESSAGE % escape_cdata(record.getMessage())

        # FIXME: Support an NDC somehow
        event['ndc'] = LOG4J_NDC % ''
        #ndc = self.get_ndc(record)
        #if ndc:
        #    event['ndc'] = LOG4J_NDC % escape_cdata(ndc)

        event['throwable'] = ''
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            event['throwable'] = LOG4J_THROWABLE % escape_cdata(record.exc_text)

        location_info = dict(pathname=cgi.escape(record.pathname),
                             lineno=record.lineno,
                             module=cgi.escape(record.module), funcName='')
        if hasattr(record, 'funcName'):
            # >= Python 2.5
            location_info['funcName'] = cgi.escape(record.funcName)
        event['locationInfo'] = LOG4J_LOCATIONINFO % location_info
        
        if self.properties is not None:
            domain_info = dict(hostname=self.properties.hostname,
                               application=self.properties.application)
            event['domainInfo'] = LOG4J_DOMAININFO % domain_info
        else:
            event['domainInfo'] = ''

        log4j_log_message = LOG4J_EVENT % event
        return log4j_log_message

def escape_cdata(cdata):
    return cdata.replace(']]>', ']]>]]&gt;<![CDATA[')

# General logging information
LOG4J_EVENT = """\
<log4j:event logger="%(name)s" timestamp="%(created)i" level="%(levelname)s" thread="%(threadName)s">
%(message)s%(ndc)s%(throwable)s%(locationInfo)s%(domainInfo)s</log4j:event>
"""

# The actual log message
LOG4J_MESSAGE = """\
    <log4j:message><![CDATA[%s]]></log4j:message>
"""

# log4j's 'Nested Diagnostic Context': additional, customizable information
# included with the log record
LOG4J_NDC = """\
    <log4j:ndc><![CDATA[%s]]></log4j:ndc>
"""

# Exception information, if exc_info was included with the record
LOG4J_THROWABLE = """\
    <log4j:throwable><![CDATA[%s]]></log4j:throwable>
"""

# Traceback information
LOG4J_LOCATIONINFO = """\
    <log4j:locationInfo class="%(module)s" method="%(funcName)s" file="%(pathname)s" line="%(lineno)d"/>
"""

# Domain information
LOG4J_DOMAININFO = """\
    <log4j:properties>
        <log4j:data name="hostname" value="%(hostname)s"/>
        <log4j:data name="application" value="%(application)s"/>
    </log4j:properties>
"""
