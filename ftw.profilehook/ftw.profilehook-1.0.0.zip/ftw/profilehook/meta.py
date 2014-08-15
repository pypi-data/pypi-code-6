from ftw.profilehook.interfaces import IProfileHook
from zope.component import zcml
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
import zope.schema


class IRegisterHook(Interface):
    """Register an upgrade step which imports a generic setup profile
    specific to this upgrade step.
    """

    profile = zope.schema.TextLine(
        title=u"GenericSetup profile id",
        required=True)

    handler = GlobalObject(
        title=u'Handler',
        description=u'',
        required=True)


def registerHook(_context, profile, handler):
    def factory(site):
        return handler

    _context.action(
        discriminator=('profile', profile),
        callable=zcml.handler,
        args=('registerAdapter',
              factory, [Interface], IProfileHook, profile, _context.info))
