from record import DTAValueError
from records import DTARecord890


class DTA(object):

    def __init__(self):
        self.records = []

    def generate(self):
        self.check()

        output = ''
        total_record = self.records.pop()
        self.records.sort(key=lambda x: (x.header.processing_date,
            x.header.sender_id, x.header.client_clearing_nr))
        self.records.append(total_record)
        for record in self.records:
            record.check()
            output += record.generate() + '\r\n'
        output = output.encode('latin-1')
        return output

    def check(self):
        if len(self.records) < 2:
            raise DTAValueError('The must be at least two records')
        if not isinstance(self.records[-1], DTARecord890):
            raise DTAValueError('Last record must be total record (type 890)')
