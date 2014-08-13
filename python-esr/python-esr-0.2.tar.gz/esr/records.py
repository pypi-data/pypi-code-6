from decimal import Decimal
from utils import format_esr_nr, parse_date_string

__all__ = ['ESRRecord', 'ESRRecordType3', 'ESRTotalRecordType3',
           'ESRRecordType4', 'ESRTotalRecordType4', 'ESRValueError']


class ESRRecord(object):
    '''
    Generic ESR record

    Instance variables (common to both type 3 and 4):
        transaction_code
        customer_nr
        reference
        amount
        price
    '''

    def __init__(self):
        self.transaction_code = None
        self.customer_nr = None
        self.reference = None
        self.amount = None
        self.price = None

    @classmethod
    def parse(cls, line):
        raise NotImplementedError()

    @classmethod
    def raise_value_error(cls, field, value):
        raise ESRValueError("Invalid %s '%s'" % (field, value))


class ESRRecordType3Base(ESRRecord):

    transaction_codes = []

    @classmethod
    def parse(cls, line):
        record = cls()

        if len(line) not in (100, 126):
            raise ValueError('Invalid line length')

        record.transaction_code = line[0:3]
        if record.transaction_code not in cls.transaction_codes:
            cls.raise_value_error('transaction code', record.transaction_code)

        record.customer_nr = format_esr_nr(line[3:12])

        return record


class ESRRecordType3(ESRRecordType3Base):
    '''
    ESR record type 3

    Instance variables:
        transaction_code
        customer_nr
        reference
        amount
        issue_date
        processing_date
        credit_date
        microfilm_nr
        reject_code
        price
    '''

    transaction_codes = [slip_type + transaction_type
        for slip_type in ('00', '01', '02', '03', '10', '11', '13')
        for transaction_type in ('2', '5', '8')]
    reject_codes = [0, 1, 5]

    # clean up class attributes
    del slip_type
    del transaction_type

    @classmethod
    def parse(cls, line):
        record = super(ESRRecordType3, cls).parse(line)

        record.reference = str(int(line[12:39]))
        record.amount = Decimal(line[39:47] + '.' + line[47:49])
        record.issue_date = parse_date_string(line[59:65])
        record.processing_date = parse_date_string(line[65:71])
        record.credit_date = parse_date_string(line[71:77])
        record.microfilm_nr = int(line[77:86])

        record.reject_code = int(line[86])
        if record.reject_code not in cls.reject_codes:
            cls.raise_value_error('reject code', record.reject_code)

        record.price = Decimal(line[96:98] + '.' + line[98:100])

        return record


class ESRTotalRecordType3(ESRRecordType3Base):
    '''
    ESR total record type 3

    Instance variables:
        transaction_code
        customer_nr
        amount
        transaction_count
        creation_date
        price
        price_esr_plus
    '''

    transaction_codes = ['999']

    @classmethod
    def parse(cls, line):
        record = super(ESRTotalRecordType3, cls).parse(line)

        record.amount = Decimal(line[39:49] + '.' + line[49:51])
        record.transaction_count = int(line[51:63])
        record.creation_date = parse_date_string(line[63:69])
        record.price = Decimal(line[69:76] + '.' + line[76:78])
        record.price_esr_plus = Decimal(line[78:85] + '.' + line[85:87])

        return record


class ESRRecordType4Base(ESRRecord):

    transaction_codes = []
    origins = []
    delivery_types = [1, 2, 3]
    currencies = ['CHF', 'EUR']

    @classmethod
    def parse(cls, line):
        record = cls()

        if len(line) != 200:
            raise ValueError('Invalid line length')

        record.transaction_code = line[0:3]
        if record.transaction_code not in cls.transaction_codes:
            cls.raise_value_error('transaction code', record.transaction_code)

        record.origin = int(line[3:5])
        if record.origin not in cls.origins:
            cls.raise_value_error('origin', record.origin)

        record.delivery_type = int(line[5])
        if record.delivery_type not in cls.delivery_types:
            cls.raise_value_error('delivery type', record.delivery_type)

        record.customer_nr = format_esr_nr(line[6:15])

        record.amount_currency = line[42:45]
        if record.amount_currency not in cls.currencies:
            cls.raise_value_error('amount currency', record.amount_currency)

        record.amount = Decimal(line[45:55] + '.' + line[55:57])

        return record


class ESRRecordType4(ESRRecordType4Base):
    '''
    ESR record type 4

    Instance variables:
        transaction_code
        origin
        delivery_type
        customer_nr
        reference
        amount_currency
        amount
        financial_institution
        issue_date
        processing_date
        credit_date
        reject_code
        price_currency
        price
    '''

    transaction_codes = [slip_type + transaction_type
        for slip_type in ('01', '02', '03', '11', '13', '21', '23', '31', '33')
        for transaction_type in ('1', '2', '3')]
    origins = [1, 2, 3, 4]
    reject_codes = [0, 1, 5]

    # clean up class attributes
    del slip_type
    del transaction_type

    @classmethod
    def parse(cls, line):
        record = super(ESRRecordType4, cls).parse(line)

        record.reference = str(int(line[15:42]))
        record.financial_institution = line[57:92]
        record.issue_date = parse_date_string(line[92:100], type=4)
        record.processing_date = parse_date_string(line[100:108], type=4)
        record.credit_date = parse_date_string(line[108:116], type=4)

        record.reject_code = int(line[116])
        if record.reject_code not in cls.reject_codes:
            cls.raise_value_error('reject code', record.reject_code)

        record.price_currency = line[117:120]
        if record.price_currency not in cls.currencies:
            cls.raise_value_error('price currency', record.price_currency)

        record.price = Decimal(line[120:124] + '.' + line[124:126])

        return record


class ESRTotalRecordType4(ESRRecordType4Base):
    '''
    ESR total record type 4

    Instance variables:
        transaction_code
        origin
        delivery_type
        customer_nr
        amount_currency
        amount
        transaction_count
        creation_date
        price_currency
        price
    '''

    transaction_codes = [slip_type + transaction_type
        for slip_type in ('99', '98')
        for transaction_type in ('1', '2')]
    origins = [99]

    # clean up class attributes
    del slip_type
    del transaction_type

    @classmethod
    def parse(cls, line):
        record = super(ESRTotalRecordType4, cls).parse(line)

        record.transaction_count = int(line[57:69])
        record.creation_date = parse_date_string(line[69:77], type=4)

        record.price_currency = line[77:80]
        if record.price_currency not in cls.currencies:
            cls.raise_value_error('price currency', record.price_currency)

        record.price = Decimal(line[80:89] + '.' + line[89:91])

        return record


class ESRValueError(Exception):
    pass
