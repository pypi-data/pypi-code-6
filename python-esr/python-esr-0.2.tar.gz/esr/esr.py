from decimal import InvalidOperation


class ESR(object):

    def __init__(self):
        self.records = []
        self.total_record = None

    @classmethod
    def parse(cls, data):
        esr = cls()
        lines = data.splitlines()

        if len(lines) < 2:
            raise ValueError('Too few lines in ESR data')

        if len(lines[0]) in (100, 126):
            from records import ESRRecordType3 as ESRRecord
            from records import ESRTotalRecordType3 as ESRTotalRecord
        elif len(lines[0]) == 200:
            from records import ESRRecordType4 as ESRRecord
            from records import ESRTotalRecordType4 as ESRTotalRecord
        else:
            raise ValueError('Invalid ESR format')

        try:
            for i, line in enumerate(lines[:-1]):
                record = ESRRecord.parse(line)
                esr.records.append(record)

            esr.total_record = ESRTotalRecord.parse(lines[-1])
            return esr
        except (TypeError, ValueError, InvalidOperation):
            raise LineMalformedError('Line %s malformed' % i)


class LineMalformedError(Exception):
    pass
