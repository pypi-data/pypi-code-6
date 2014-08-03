from zope.interface import Interface, Attribute
from twisted.plugin import IPlugin

class ISubCommand(Interface, IPlugin):
    name = Attribute("""The command name, as carml will refer to it.""")
    options_class = Attribute("""Factory for your twisted.usage.Options subclass.""")
    help_text = Attribute("""Something useful to tell the user.""")

    controller_connection = Attribute("""If False, don't build a TorControlProtocol connection at all (and also then implies build_state == False)""")
    build_state = Attribute("""If True, also build a TorState instance on startup. This takes a second or two to load all the Router instances (but see load_routers).""")
    load_routers = Attribute("""Passed to TorState if build_state was True, this controls whether Routers are queried. If not, the only information valid in Router instances will be name and id_hash""")

    def validate(options, main_options):
        """
        Should either raise an exception with a nice error-message for
        the user, or do nothing if the options are acceptable
        """

    def __call__(options, mainoptions, arg):
        """
        After the Tor connection (and possible bootstrapping of
        TorState) is complete, this will be called with...

        :param arg:
            ...a TorControlProtocol instance (or a TorState instance
            if build_state is set to True).
        
        :param options:
            an instance of your options class.

        :param mainoptions: 
            an instance of the main command's option class
            (dispatch.Options)

        This method is expected to arrange for reactor.stop() to get
        called so the process exits (or not, for example to monitor
        messages).

        There is no return value.
        """
