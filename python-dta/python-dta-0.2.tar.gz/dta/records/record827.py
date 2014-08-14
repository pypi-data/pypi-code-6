from dta import DTARecord, fields


class DTARecord827(DTARecord):

    reference = fields.AlphaNumeric(11)
    liability_account = fields.AlphaNumeric(24)
    currency = fields.AlphaNumeric(3)
    amount = fields.Currency(12)

    client_address1 = fields.AlphaNumeric(24, clipping=True)
    client_address2 = fields.AlphaNumeric(24, required=False)
    client_address3 = fields.AlphaNumeric(24, clipping=True)
    client_address4 = fields.AlphaNumeric(24, clipping=True)

    recipient_account = fields.AlphaNumeric(27)
    recipient_address1 = fields.AlphaNumeric(24, clipping=True)
    recipient_address2 = fields.AlphaNumeric(24, required=False)
    recipient_address3 = fields.AlphaNumeric(24, clipping=True)
    recipient_address4 = fields.AlphaNumeric(24, clipping=True)

    message1 = fields.AlphaNumeric(28, required=False)
    message2 = fields.AlphaNumeric(28, required=False)
    message3 = fields.AlphaNumeric(28, required=False)
    message4 = fields.AlphaNumeric(28, required=False)

    beneficiary_account = fields.AlphaNumeric(27, required=False)
    beneficiary_address1 = fields.AlphaNumeric(24, required=False,
        clipping=True)
    beneficiary_address2 = fields.AlphaNumeric(24, required=False,
        clipping=True)
    beneficiary_address3 = fields.AlphaNumeric(24, required=False,
        clipping=True)
    beneficiary_address4 = fields.AlphaNumeric(24, required=False,
        clipping=True)

    def __init__(self, header):
        super(DTARecord827, self).__init__()
        self.header = header
        self.header.transaction_code = 827

    def generate(self):
        super(DTARecord827, self).generate()
        seg01 = ''.join(['01',
            self.header.generate(),
            self.header.sender_id,
            self.reference,
            self.liability_account,
            '      ',  # valuta not required
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
            ' ' * 30,  # reserved
            ])
        assert len(seg02) == 128

        seg03 = ''.join(['03',
            '/C/' + self.recipient_account,
            self.recipient_address1,
            self.recipient_address2,
            self.recipient_address3,
            self.recipient_address4,
            ])
        assert len(seg03) == 128

        segments = [seg01, seg02, seg03]

        if any(f.strip() for f in [self.message1, self.message2, self.message3,
                self.message4, self.beneficiary_account]):
            seg04 = ''.join(['04',
                self.message1,
                self.message2,
                self.message3,
                self.message4,
                ' ' * 14,  # reserved
                ])
            assert len(seg04) == 128
            segments.append(seg04)

        if self.beneficiary_account.strip():
            seg05 = ''.join(['05',
                '/C/' + self.beneficiary_account,
                self.beneficiary_address1,
                self.beneficiary_address2,
                self.beneficiary_address3,
                self.beneficiary_address4,
                ])
            assert len(seg05) == 128
            segments.append(seg05)

        return '\r\n'.join(segments)
