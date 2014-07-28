from qsdn import QSDNLocale as IQLocale
from qsdn import QSDNNumericValidator as CryptoCurrencyValidator
import unittest
from decimal import Decimal as D
import decimal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class NumberOption(unittest.TestCase):
    def setUp(self):
        self.rc_locale = IQLocale()
        self.rc_locale.setNumberOptions( QLocale.NumberOptions(QLocale.RejectGroupSeparator) )
        self.oc_locale = IQLocale()
        self.oc_locale.setNumberOptions( QLocale.NumberOptions(QLocale.OmitGroupSeparator) )
        
    def test_noOption(self):
        self.assertFalse(self.rc_locale is self.oc_locale)
        default_locale = IQLocale()
        self.assertFalse( default_locale.numberOptions() == QLocale.NumberOptions(QLocale.OmitGroupSeparator) )
        self.assertFalse( default_locale.numberOptions() == QLocale.NumberOptions(QLocale.RejectGroupSeparator) )
        self.assertNotEqual(QLocale.OmitGroupSeparator, QLocale.RejectGroupSeparator)
        self.assertFalse( default_locale.numberOptions() & QLocale.NumberOptions(QLocale.RejectGroupSeparator) == QLocale.NumberOptions(QLocale.RejectGroupSeparator) )
        self.assertFalse( default_locale.numberOptions() & QLocale.NumberOptions(QLocale.OmitGroupSeparator) == QLocale.NumberOptions(QLocale.OmitGroupSeparator) )
        self.assertFalse( default_locale.numberOptions() & QLocale.RejectGroupSeparator == QLocale.RejectGroupSeparator )
        self.assertFalse( default_locale.numberOptions() & QLocale.OmitGroupSeparator == QLocale.OmitGroupSeparator )

    def test_RejCommaOption(self):
        self.assertFalse(self.rc_locale.numberOptions() == QLocale.OmitGroupSeparator )
        self.assertTrue(self.rc_locale.numberOptions() & QLocale.RejectGroupSeparator == QLocale.RejectGroupSeparator)    
        self.assertTrue(self.rc_locale.numberOptions() & QLocale.OmitGroupSeparator == QLocale.NumberOptions(0)) 
            
    def test_omit_group_separator_option(self):
        self.assertEqual(self.oc_locale.numberOptions() & QLocale.NumberOptions(QLocale.OmitGroupSeparator), QLocale.NumberOptions(QLocale.OmitGroupSeparator))
        self.assertNotEqual(self.oc_locale.numberOptions() & QLocale.RejectGroupSeparator, QLocale.RejectGroupSeparator)

def test_data_group(self, name, validator, test_set):
    	TESTINPUT=0
    	EXPECTED=1    	
        for test_case in test_set:
            modified_string = QString(test_case[TESTINPUT][0])
            (status, pos) = validator.validate(modified_string, test_case[TESTINPUT][1])
	    if status == QValidator.Invalid:
		self.assertEqual( test_case[EXPECTED][1], status, name + test_case[TESTINPUT][0] + '=>' + test_case[EXPECTED][0] + ' (status == QValidator.Invalid)')
	    elif status == QValidator.Intermediate:
		self.assertEqual( test_case[EXPECTED][1], status, name + test_case[TESTINPUT][0] + '=>' + test_case[EXPECTED][0] + ' (status == QValidator.Intermediate)')
	    else:
		self.assertEqual( test_case[EXPECTED][1], status, name + test_case[TESTINPUT][0] + '=>' + test_case[EXPECTED][0] + ' (status == QValidator.Acceptable)')
	    if test_case[EXPECTED][1] == QValidator.Acceptable and status == QValidator.Acceptable:
	    	if pos != test_case[EXPECTED][2]: 
	    	    exp_pos = test_case[EXPECTED][2] 
	    	    print ''
	    	    print str(test_case[EXPECTED][0])
	    	    if exp_pos < pos:
			print exp_pos * ' ' + '^' + (pos -exp_pos - 1) * ' ' + '^'
			print exp_pos * ' ' + '+-- expected '
			print pos * ' ' +  '+-- actual pos'
		    else:
			print pos * ' ' + '^' + (exp_pos - pos - 1) * ' ' + '^'
			print exp_pos * ' ' + '+-- expected '
			print pos * ' ' +  '+-- actual pos'
		    self.assertTrue(False, ' (pos was not expected)')
		self.assertEqual( test_case[EXPECTED][0], modified_string, name + str(test_case[TESTINPUT][0]) + '=>' + str(test_case[EXPECTED][0]) + ' (string)' )
    	


class TestNumericFormating(unittest.TestCase):
    
    def test_all(self):  
    	TESTINPUT=0
    	EXPECTED=1    	
        

        context = decimal.getcontext()
        context.prec = 8+7
        decimal.setcontext(context)
        tests = ( (decimal.Decimal("43112279.75467"), "43,112,279.754,67"), (decimal.Decimal("0.0101020204"), "0.010,102,020,4"),
            (decimal.Decimal("0.00000001"), "0.000,000,01")
            )
        locale = IQLocale("US")
        QLocale.setDefault(locale)
        verbose = False
        for c in tests:
            self.assertEqual( QString(c[1]), locale.toString(c[0]), msg="Test case %s" % c[1] )
        
        new_string = '0xFF0'
 	(value, ok) = locale.toDecimal(new_string)
	self.assertEqual( new_string, '0xFF0', msg = 'numbers passed are not modified')
	a_string = QString('      100')
	another_string = QString(a_string)
	locale.toDecimal(a_string)
	self.assertFalse( a_string is another_string)
	self.assertEqual( a_string, another_string, msg = "toDecimal doesn't modify string")
	self.assertEqual( ok,    True,  msg = "hex numbers without commas parse successfully")
	self.assertEqual( value, 0xFF0, msg = "hex numbers without commas parse correctly")
	(value, ok) = locale.toDecimal( QString("") )
	self.assertEqual( ok, False )
	(value, ok) = locale.toDecimal( QString("The cat came back ") )
	self.assertEqual( ok, False )


        # no commas:
        us_locale_no_comma = IQLocale("US")
        us_locale_no_comma.setNumberOptions( QLocale.NumberOptions(QLocale.OmitGroupSeparator) )
        for c in tests:
            self.assertEqual( QString(c[1]).remove(','), us_locale_no_comma.toString(c[0]), 
                msg ="Test case %s" % c[1] )
        
        if verbose:
            try:
                spanishlocale = IQLocale("es_ES")
                print "Using %s locale" % spanishlocale.name()
                for c in tests:
                    print "The value %s is %s" % (c[1], spanishlocale.toString(c[0]))
            except:
                print "Could not get a Spanish locale to show you what they look like.  too bad."
                
            try:
                koreanlocale = IQLocale("kr")
                print "Using %s locale" % koreanlocale.name()
                for c in tests:
                    print "The value %s is %s" % (c[1], koreanlocale.toString(c[0]))
            except:
                print "Could not get a Korean locale to show you what they look like.  too bad."
                
            try:
                clocale = IQLocale("C")
                print "Using %s locale" % clocale.name()
                for c in tests:
                    print "The value %s is %s" % (c[1], clocale.toString(c[0]))
            except:
                print "Could not get the C locale to show you what they look like.  too bad."
            
            
            print "The locale your system is using is %s" % QLocale.system().name()
            
        (d, good) = locale.toDecimal(QString("7,423,231,123"), 10)
        self.assertEqual( True, good, msg="7 billion #1" )
        self.assertEqual( decimal.Decimal("7423231123"), d , msg="7 billion #2" )
        self.assertEqual( "7,423,231,123", locale.toString(d) , msg="7 billion #3" )
        
        (d, good) = locale.toDecimal(QString("0xB,ADF,00D"))
        self.assertEqual( True, good, msg="0xB,ADF,00D #1" )
        self.assertEqual( decimal.Decimal("195948557"), d, msg="0xB,ADF,00D #2" )
        self.assertEqual( (decimal.Decimal("0.3125"), True), locale.toDecimal("0x0.5"), msg="5/16 hex #1" ) # 5/16
        self.assertEqual( (decimal.Decimal("0.3125"), True), locale.toDecimal("0.5", 16), msg="5/16 hex #2" ) # 5/16
        self.assertEqual( (D("1.25"), True), locale.toDecimal("01.2"), msg="1 1/4 octal #1" )  # 1 1/4
        self.assertEqual( (D("1.25"), True), locale.toDecimal("1.2", 8), msg="1 1/4 octal #2" )  # 1 1/4
        self.assertEqual( (D("1.2"), True), locale.toDecimal(QString("01.2"), 10), msg="1 1/5 decimal #1" )	# 1 1/5
        self.assertEqual((D("1.2"), True), locale.toDecimal(QString("1.2")), msg="1 1/5 decimal #2" )	# 1 1/5
        self.assertEqual( (D("6.375"), True), locale.toDecimal("110.011", 2), msg="4+2+1/4+1/8 binary" )
        self.assertEqual( "12.00", locale.toString(decimal.Decimal("12").quantize(D('0.01'))), msg="12 dollars" )
        self.assertEqual( "3,379.70", locale.toString(decimal.Decimal("3379.7").quantize(D('0.01'))) , msg="rubbles" )
        self.assertEqual( "636.40", locale.toString(decimal.Decimal("636.4").quantize(D('0.01'))), msg= "cny" )
        self.assertEqual( "67.56", locale.toString(decimal.Decimal("67.56")), msg= "GBP" )
        self.assertEqual( "103.00", locale.toString(decimal.Decimal("103").quantize(D('0.01'))), msg= "USD" )
        self.assertEqual( "1,000,000", locale.toString(decimal.Decimal(10)**6), msg= "1 million" )
        context.prec = 30
        decimal.setcontext(context)
        self.assertEqual( "0.333,33", locale.toString((decimal.Decimal("1")/3).quantize(D('0.00001'))) , msg= "1/3" )
        self.assertEqual( "0.50", locale.toString(decimal.Decimal("1").quantize(D('0.01'))/2), msg= "1/2" )
        #
        #
        #	print "0.003,2 tests as valid: good."
        validator = CryptoCurrencyValidator(8, 8, True)
        validator.setLocale( IQLocale("US") )
        
        
        
        validator_test_data =  [  \
                ((QValidator.Acceptable, "0.003,4"), "0.0034"), \
                ((QValidator.Acceptable, "0.001,423"), "0.001,423"), \
        ((QValidator.Acceptable, "0.003,412,3"), "0.003,412,3"), \
        ((QValidator.Intermediate, "123,456,789"), "123456789"), \
        ((QValidator.Acceptable, "0.013,410"), "0.013410"), \
        ((QValidator.Intermediate, "0.123,"), "0.123,"), \
        ((QValidator.Acceptable, "0.42"), ".42"),
        ((QValidator.Invalid, "0123.12.3"), "0123.12.3") ]
        
        validate_strings = [ 'QValidator.Invalid', 'QValidator.Intermediate', 'QValidator.Acceptable' ]
        (status, pos) = validator.validate(QString(""), 0)
        self.assertEqual( QValidator.Intermediate, status, msg="Validate validate partial string #0" )
        for test_case_type in validator_test_data:
            result_string = QString(test_case_type[1])
            (status, pos) = validator.validate(result_string, 0)
            if status == QValidator.Acceptable:
            	if status != test_case_type[0][0]:
            	    print "status is %s.  it should be %s " % (validate_strings[status], validate_strings[ test_case_type[0][0] ] )
		    self.assertTrue( False, msg=test_case_type[1] + "=>" + test_case_type[0][1] + " status" )
		# print "status is ", status == QValidator.Acceptable
		if test_case_type[0][0] == QValidator.Acceptable:
		    self.assertEqual( test_case_type[0][1], result_string.trimmed(), msg=test_case_type[1] + "=>" + test_case_type[0][1] + " string" )
                
        egyptian = IQLocale( QLocale( QLocale.Arabic, QLocale.Egypt ) )
        self.assertEqual( QString(u'\u0663\u066b\u0661\u0664\u0661\u066c\u0666'), egyptian.toString( decimal.Decimal('3.1416') ) , msg= "Egyptian PI 5 digits" )
        
        spacing_validator = CryptoCurrencyValidator(8, 8, True)
        spacing_validator.setLocale( IQLocale("US") )
        self.validator = spacing_validator
        self.name = 'spaced'
        spaced_test_set = [  [["1", 1], ["         1", QValidator.Acceptable, 10]], \
                      [[9*' '+"17", 11], [8*' '+"17", QValidator.Acceptable, 10]],\
                      [[8*' '+"17,", 11], [8*' '+"17,", QValidator.Intermediate, 11]],\
                      [[8*' '+"177", 11], [7*' '+"177", QValidator.Acceptable, 10]], \
                      [[7*' '+"177,", 11], [7*' '+"177,", QValidator.Intermediate, 11]], \
                      [[7*' '+"1777", 11], [5*' '+"1,777", QValidator.Acceptable, 10]], \
                      [[5*' '+"1,7772", 11], [4*' '+"17,772", QValidator.Acceptable, 10]], \
                      [["    17,7721", 11], [3*' '+"177,721", QValidator.Acceptable, 10]], \
                  [["   177,7216", 11], [" 1,777,216", QValidator.Acceptable, 10]], \
                  [["123456789", 4], ["123,456,789", QValidator.Intermediate, 5]], \
                  [["0.013410", 7], [9*' '+"0.013,410", QValidator.Acceptable, 17]], \
                  [["0.0034", 2], [9*' '+"0.003,4", QValidator.Acceptable, 11]], \
                  [["1", 0], [' '*9+"1", QValidator.Acceptable, 0]], \
                  [["0", 1], [9*' '+"0", QValidator.Acceptable, 10]], \
                  [['23124', 3], ["    23,124", QValidator.Acceptable, 8]], \
                  [['%!@', 2], ["%!@", QValidator.Invalid, 2]], \
                  [['        0.471,400', 8], ['         0.471,400', QValidator.Acceptable, 9]], \
                  [['11,213,421.000,1', 0], ['11,213,421.000,1', QValidator.Acceptable, 0]], \
                  [['        100', 11], ['       100', QValidator.Acceptable, 10]], \
                  [[' 1,000,000', 9], [' 1,000,000', QValidator.Acceptable, 9]], \
                  [['Hello', 2], ['Hello', QValidator.Invalid, 2] ] \
        ]
        self.test_set = spaced_test_set
	test_data_group(self, self.name, self.validator, self.test_set)                  

        no_spaces = CryptoCurrencyValidator(8, 8, False)
        no_spaces.setLocale( IQLocale("US") )
        test_data_group(self, 'no spaces', no_spaces, [  [["1", 1], ["1", QValidator.Acceptable, 1]], \
        [["17", 2], ["17", QValidator.Acceptable, 2]],\
        [["17,", 3], ["17,", QValidator.Intermediate, 3]],\
        [["177", 3], ["177", QValidator.Acceptable, 3]], \
        [["177,", 4], ["177,", QValidator.Intermediate, 4]], \
        [["1777", 4], ["1,777", QValidator.Acceptable, 5]], \
        [["1,7772", 6], ["17,772", QValidator.Acceptable, 6]], \
        [["17,7721", 7], ["177,721", QValidator.Acceptable, 7]], \
        [["177,7216", 8], ["1,777,216", QValidator.Acceptable, 9]], \
        [["23456789", 4], ["23,456,789", QValidator.Acceptable, 5]], \
        [["0.013410", 7], ["0.013,410", QValidator.Acceptable, 8]], \
        [["0.000,000,001", 14], ["0.000,000,001", QValidator.Intermediate, 14]], \
        [["0.000,000,000,001", 18], ["0.000,000,000.001", QValidator.Intermediate, 18]], \
        [["10,000,0000", 12], ["100,000,000", QValidator.Intermediate, 12]], \
        [["0.0034", 2], ["0.003,4", QValidator.Acceptable, 2]], \
        [["1", 1], ["1", QValidator.Acceptable, 1]], \
        [["0", 0], ["0", QValidator.Acceptable, 0]], \
        [['23124', 3], ["23,124", QValidator.Acceptable, 4]], \
        [['%!@', 2], ["%!@", QValidator.Invalid, 2]], \
        [["0.003,2", 0], ["0.003,2", QValidator.Acceptable, 0]], \
        [['Hello', 2], ['Hello', QValidator.Invalid, 2] ] \
          ])


class TestConversion(unittest.TestCase):
    def test_all(self):
    	locale = IQLocale('US')
    	locale.toShort('321')
    	self.assertEqual( (321, True) , locale.toShort('321', 10), msg = "tiny value to short")
    	self.assertEqual( False, locale.toShort('70,000', 10)[1], msg = "value to to short is too long")
	self.assertEqual( (32000, True), locale.toShort('32,000', 10), msg = "big value to short")
        self.assertEqual( (60000, True), locale.toUShort('60,000', 10), msg = "big value to ushort")
	self.assertEqual( (2000000, True), locale.toInt('2,000,000', 10), msg = "big int value to int")
	self.assertEqual( (4000000, True), locale.toUInt('4,000,000', 10), msg = "big uint value to int")
if __name__ == '__main__':
    unittest.main()


