from dta import DTARecord, DTAValueError, fields


class DTARecord836(DTARecord):

    reference = fields.AlphaNumeric(11)
    liability_account = fields.AlphaNumeric(24)
    valuta = fields.Date()
    currency = fields.AlphaNumeric(3)
    amount = fields.Currency(15)

    exchange_rate = fields.Currency(12, required=False)
    client_address1 = fields.AlphaNumeric(35, clipping=True)
    client_address2 = fields.AlphaNumeric(35, clipping=True)
    client_address3 = fields.AlphaNumeric(35, clipping=True)

    bank_address_type = fields.AlphaNumeric(1)
    bank_address1 = fields.AlphaNumeric(35, required=False)
    bank_address2 = fields.AlphaNumeric(35, required=False)
    recipient_iban = fields.AlphaNumeric(34)

    recipient_address1 = fields.AlphaNumeric(35, clipping=True)
    recipient_address2 = fields.AlphaNumeric(35, clipping=True)
    recipient_address3 = fields.AlphaNumeric(35, clipping=True)

    payment_reason_type = fields.AlphaNumeric(1, default='U')
    payment_reason1 = fields.AlphaNumeric(35, required=False)
    payment_reason2 = fields.AlphaNumeric(35, required=False)
    payment_reason3 = fields.AlphaNumeric(35, required=False)
    charges_handling = fields.Numeric(1)

    def __init__(self, header):
        super(DTARecord836, self).__init__()
        self.header = header
        self.header.transaction_code = 836

    def generate(self):
        super(DTARecord836, self).generate()
        seg01 = ''.join(['01',
            self.header.generate(),
            self.header.sender_id,
            self.reference,
            self.liability_account,
            self.valuta,
            self.currency,
            self.amount,
            ' ' * 11,  # reserved
            ])
        assert len(seg01) == 128

        seg02 = ''.join(['02',
            self.exchange_rate,
            self.client_address1,
            self.client_address2,
            self.client_address3,
            ' ' * 9,  # reserved
            ])
        assert len(seg02) == 128

        seg03 = ''.join(['03',
            self.bank_address_type,
            self.bank_address1,
            self.bank_address2,
            self.recipient_iban,
            ' ' * 21,  # reserved
            ])
        assert len(seg03) == 128

        seg04 = ''.join(['04',
            self.recipient_address1,
            self.recipient_address2,
            self.recipient_address3,
            ' ' * 21,  # reserved
            ])
        assert len(seg04) == 128

        seg05 = ''.join(['05',
            self.payment_reason_type,
            self.payment_reason1,
            self.payment_reason2,
            self.payment_reason3,
            self.charges_handling,
            ' ' * 19,  # reserved
            ])
        assert len(seg05) == 128

        return '\r\n'.join((seg01, seg02, seg03, seg04, seg05))

    def check(self):
        super(DTARecord836, self).check()
        if self.bank_address_type not in ('A', 'D'):
            raise DTAValueError("Invalid bank address type '%s'" %
                self.bank_address_type)
        if self.payment_reason_type not in ('I', 'U'):
            raise DTAValueError("Invalid payment reason type '%s'" %
                self.payment_reason_type)
        if self.charges_handling not in ('0', '1', '2'):
            raise DTAValueError("Invalid charges handling value '%s'" %
                self.charges_handling)
