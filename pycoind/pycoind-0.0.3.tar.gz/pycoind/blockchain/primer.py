import struct

from ..protocol.format import FormatTypeVarString

HeaderFormat = '>8sBQII32s64s'
HeaderNames = ('magic', 'version', 'timestamp', 'start', 'length', 'checksum', 'signature')

VERSION = 1

# Magic Number:
#    PCP     PyCoindPrimer
#    \x05    ensures applications recognize it is binary (non-printable)
#    \r\n\r  ensures line "fixing" will euchre the header
#    \0      because who doesn't like null termination?
MAGIC = 'PCP\x05\r\n\r\0'


def _parse_header(header):
    data = struct.unpack(HeaderFormat, header)
    params = dict(zip(HeaderNames, data))
    (vl, coinname) = FormatTypeVarString.parse(data[117:])
    params['coinname'] = coinname
    params['offset'] = 117 + vl

    return params

def _build_header(start, length, coinname, checksum = ('\0' * 32), signature = ('\0' * 64), timestamp = None):
    if timestamp is None:
        timstamp = time.time()
    timestamp = int(timestamp)
    header = struct.pack(HeaderFormat, MAGIC, VERSION, timestamp, start, length, checksum, signature)
    header += FormatTypeVarString.binary(coinname)

    return header

class Primer(object):
    def __init__(self, blockchain):
        self._blockchain = blockchain

    @property
    def valid_range(self):
        '''The range of the blockchain that is currently complete, and
           therefore can be exported.'''
        return (1, 100)


    def export_file(self, filename, start_height = 1, max_length = None, max_filesize = None, private_key = None):
        pass


    def check_file(self, filename, public_key = None):
        pass


    def import_file(self, filename, public_key = None):
        pass
