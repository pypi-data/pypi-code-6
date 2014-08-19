import datetime

class Uptime:
    """ Returns the uptime of the system as a human-readable string """

    def getVariableTuple(self):

        with open('/proc/uptime') as fp:

            uptime_seconds = float(fp.read().split(' ')[0])
            uptime_readable = str(datetime.timedelta(seconds = uptime_seconds))

            return [('UPTIME', uptime_readable)]