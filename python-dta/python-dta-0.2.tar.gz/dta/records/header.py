from dta import DTARecord, DTAValueError, fields


class DTAHeader(DTARecord):

    processing_date = fields.Date(required=False, default='000000')
    recipient_clearing_nr = fields.AlphaNumeric(12, required=False)
    creation_date = fields.Date()
    client_clearing_nr = fields.AlphaNumeric(7, required=False)
    sender_id = fields.AlphaNumeric(5)
    sequence_nr = fields.Numeric(5)
    transaction_code = fields.Numeric(3)
    payment_type = fields.Numeric(1, default=0)

    def generate(self):
        super(DTAHeader, self).generate()
        return ''.join([
            self.processing_date,
            self.recipient_clearing_nr,
            '00000',  # output sequence number
            self.creation_date,
            self.client_clearing_nr,
            self.sender_id,
            self.sequence_nr,
            self.transaction_code,
            self.payment_type,
            '0',  # editing flag
            ])

    def check(self):
        super(DTAHeader, self).check()
        if (self.transaction_code in ['830', '832', '836', '837', '890'] and
                self.processing_date != '000000'):
            raise DTAValueError('Processing date must be empty')
        if (self.transaction_code in ['826', '827'] and
                not self.processing_date.strip()):
            raise DTAValueError('Processing date must not be empty')
        if (self.transaction_code in ('826', '830', '832', '836', '837') and
                self.recipient_clearing_nr.strip()):
            raise DTAValueError('Recipient clearing number must be empty')
        if self.transaction_code not in ('826', '827', '830', '832', '836',
                '837', '890'):
            raise DTAValueError("Invalid transaction code '%s'" %
                    self.transaction_code)
        if self.payment_type not in ('0', '1'):
            raise DTAValueError("Invalid payment type '%s'" %
                    self.payment_type)
        if (self.transaction_code in ('826', '830', '832', '890') and
                self.payment_type != '0'):
            raise DTAValueError('Payment type must be 0')
