from .records import BaseRecord, AlphaNumericField, NumericField, \
    CBIDateField, DecimalField

from .cbibon_dom import CBIRecord


class PERecord(CBIRecord):
    @classmethod
    def define_fields(cls):
        f = cls.builders()
        f.an(1, 'filler', 1)
        f.an(2, 'record_type', 2, default='PE')
        f.nu(4, 'sia', 5)
        f.nu(9, 'abi', 5)
        f.dt(14, 'creation', 6)
        f.an(20, 'name', 20)
        f.an(40, 'available', 6)
        f.an(46, 'filler2', 61)
        f.an(105, 'flow_qualifier', 7)
        f.an(112, 'filler3', 9)


class EFRecord(CBIRecord):
    @classmethod
    def define_fields(cls):
        f = cls.builders()
        f.an(1, 'filler', 1)
        f.an(2, 'record_type', 2, default='EF')
        f.an(4, 'sender', 5)
        f.nu(9, 'recipient', 5)
        f.dt(14, 'creation', 6)
        f.an(20, 'name', 20)
        f.an(40, 'available', 6)
        f.nu(46, 'orders', 7)
        f.an(53, 'filler2', 12)
        f.cur(65, 'amounts', 18)
        f.nu(83, 'records', 7)
        f.an(90, 'filler3', 25)
        f.an(115, 'not_available', 6)


class PaymentIdDates(CBIRecord):
    @classmethod
    def define_fields(cls):
        f = cls.builders()
        f.an(1, 'filler', 1)
        f.an(2, 'record_type', 2, default='H1')
        f.an(4, 'prog_number', 7)
        f.an(11, 'msg_identifier', 14, default='PAYORDD  93AUN')
        f.an(25, 'msg_name', 3, default='450')
        f.an(28, 'reference', 34)
        f.an(62, 'filler2', 1)
        f.an(63, 'msg_type', 2, default='9 ')
        f.nu(65, 'creation_date_qualifier')
        f.dt(68, 'creation_date', 8)
        f.nu(76, 'creation_date_format', 3, default=102)
        f.nu(79, 'execution_date_qualifier', 3)
        f.dt(82, 'execution_date', 8)
        f.nu(90, 'execution_date_format', 3, default=102)
        f.nu(93, 'availability_date_qualifier', 3)
        f.dt(96, 'availability_date', 8)
        f.nu(104, 'availability_date_format', 3, default=102)
        f.an(107, 'transaction_type', 3, default='IN ')
        f.an(110, 'payment_type', 3)
        f.an(113, 'filler3', 3)
        f.an(116, 'not_available', 5)


class PaymentMode(CBIRecord):
    @classmethod
    def define_fields(cls):
        f = cls.builders()
        f.an(1, 'filler', 1)
        f.an(2, 'record_type', 2, default='P0')
        f.an(4, 'prog_number', 7)
        f.an(11, 'payment_form', 3)
        f.an(14, 'charges_split', 3)
        f.an(17, 'charges_account_cab', 5)
        f.an(22, 'charges_account_s1', 3, default='25 ')
        f.an(25, 'charges_account_s2', 3, default='119')
        f.an(28, 'charges_account_code', 17)
        f.an(45, 'charges_account_cin', 1)
        f.an(46, 'filler2', 75)


class PaymentAmount(CBIRecord):
    @classmethod
    def define_fields(cls):
        f = cls.builders()
        f.an(1, 'filler', 1)
        f.an(2, 'record_type', 2, default='P1')
        f.an(4, 'prog_number', 7)
        f.an(11, 'currency_relationship', 3, default='9  ')
        f.cur(14, 'amount', 18)
        f.an(32, 'currency', 3, default='EUR')
        f.an(35, 'charge_currency_qualifier', 3)
        f.an(38, 'charge_currency', 3)
        f.an(41, 'charge_exchange_rate', 12)
        f.an(53, 'credit_currency_qualifier', 3)
        f.an(56, 'credit_currency', 3)
        f.an(59, 'credit_exchange_rate', 12)
        f.an(71, 'filler2', 11)
        f.an(82, 'instructions_code', 3)
        f.an(85, 'instructions_contract', 35)
        f.an(120, 'filler3', 1)


class PaymentBanks(CBIRecord):
    @classmethod
    def define_fields(cls):
        f = cls.builders()
        f.an(1, 'filler', 1)
        f.an(2, 'record_type', 2, default='PH')
        f.an(4, 'prog_number', 7)
        f.an(11, 'payer_iban', 34)
        f.an(45, 'payer_bic', 11)
        f.an(56, 'filler2', 5)
        f.an(61, 'payee_iban', 34)
        f.an(95, 'payee_bic', 11)
        f.an(106, 'filler3', 15)


class Payee(CBIRecord):
    @classmethod
    def define_fields(cls):
        f = cls.builders()
        f.an(1, 'filler', 1)
        f.an(2, 'record_type', 2, default='P5')
        f.an(4, 'prog_number', 7)
        f.an(11, 'fixed', 3, default='BE ')
        f.an(14, 'name', 35)
        f.an(49, 'address', 35)
        f.an(84, 'town', 32)
        f.an(116, 'payee_sia', 5)


class PaymentAmount(CBIRecord):
    @classmethod
    def define_fields(cls):
        f = cls.builders()
        f.an(1, 'filler', 1)
        f.an(2, 'record_type', 2, default='P1')
        f.an(4, 'prog_number', 7)








