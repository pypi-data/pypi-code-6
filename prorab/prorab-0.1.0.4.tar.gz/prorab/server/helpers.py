import json

from twisted.protocols.basic import LineReceiver


class JSONReceiver(LineReceiver):
    """
    Class inherited from twisted's LiveReceiver for dealing with json.
    """
    def jsonReceived(self, data):
        """
        Called when lineReceived, but deals with json instead of text.

        data -- json value.
        """
        pass

    def sendJson(self, data):
        """
        Send json. Dump data and sendLine.

        data -- value to dump.
        """
        self.sendLine(json.dumps(data).encode("utf-8"))

    def lineReceived(self, line):
        self.jsonReceived(json.loads(line.decode("utf-8")))
