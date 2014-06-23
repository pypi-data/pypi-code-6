from dta import DTARecord, fields


class DTARecord826(DTARecord):

    reference = fields.AlphaNumeric(11)
    liability_account = fields.AlphaNumeric(24)
    currency = fields.AlphaNumeric(3)
    amount = fields.Currency(12)

    client_address1 = fields.AlphaNumeric(20, clipping=True)
    client_address2 = fields.AlphaNumeric(20, required=False, clipping=True)
    client_address3 = fields.AlphaNumeric(20, clipping=True)
    client_address4 = fields.AlphaNumeric(20, clipping=True)

    recipient_account = fields.Numeric(9)
    recipient_address1 = fields.AlphaNumeric(20, required=False, clipping=True)
    recipient_address2 = fields.AlphaNumeric(20, required=False, clipping=True)
    recipient_address3 = fields.AlphaNumeric(20, required=False, clipping=True)
    recipient_address4 = fields.AlphaNumeric(20, required=False, clipping=True)
    esr_reference = fields.Numeric(27)
    esr_check_digit = fields.AlphaNumeric(2, required=False, default='  ')

    def __init__(self, header):
        super(DTARecord826, self).__init__()
        self.header = header
        self.header.transaction_code = 826

    def generate(self):
        super(DTARecord826, self).generate()
        seg01 = ''.join(['01',
            self.header.generate(),
            self.header.sender_id,
            self.reference,
            self.liability_account,
            ' ' * 6,  # valuta not required
            self.currency,
            self.amount,
            ' ' * 14,  # reserved
            ])
        assert len(seg01) == 128

        seg02 = ''.join(['02',
            self.client_address1,
            self.client_address2,
            self.client_address3,
            self.client_address4,
            ' ' * 46,  # reserved
            ])
        assert len(seg02) == 128

        seg03 = ''.join(['03',
            '/C/' + self.recipient_account,
            self.recipient_address1,
            self.recipient_address2,
            self.recipient_address3,
            self.recipient_address4,
            self.esr_reference,
            self.esr_check_digit,
            ' ' * 5,  # reserved
            ])
        assert len(seg03) == 128

        return '\r\n'.join((seg01, seg02, seg03))
