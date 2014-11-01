"""XMLLayout Formatter and RawSocketHandler"""

__author__    = 'Philip Jenvey <pjenvey@groovie.org>, Stojan Jovic <stojan.jovic@dmsgroup.rs>'
__contact__   = 'pjenvey@groovie.org, stojan.jovic@dmsgroup.rs'
__date__      = '12 August 2007'
__copyright__ = 'Python Software Foundation'

# Modified: 12 December 2008
from formatters import XMLLayout
from handlers import RawSocketHandler
from properties import Log4jProperties

def LogfacesFormatter(**kwds):
    props = Log4jProperties(**kwds)
    return XMLLayout(properties=props)

