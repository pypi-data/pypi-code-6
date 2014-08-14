from dta import DTARecord, fields


class DTARecord890(DTARecord):

    amount = fields.Currency(16)

    def __init__(self, header):
        super(DTARecord890, self).__init__()
        self.header = header
        self.header.transaction_code = 890
        self.header.client_clearing_nr = ' ' * 7

    def generate(self):
        super(DTARecord890, self).generate()
        seg01 = ''.join(['01',
            self.header.generate(),
            self.amount,
            ' ' * 59,  # reserved
            ])
        assert len(seg01) == 128
        return seg01
