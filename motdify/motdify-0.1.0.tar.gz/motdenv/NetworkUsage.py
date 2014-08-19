import psutil

class NetworkUsage:
    """ Returns the amount of megabytes sent/received by the system """

    def getVariableTuple(self):

        usage = psutil.net_io_counters()

        return [
            ('NET_MB_SENT', usage.bytes_sent / 1000000), # 1 MB = 1.000.000 Bytes
            ('NET_MB_RECV', usage.bytes_recv / 1000000)
        ]