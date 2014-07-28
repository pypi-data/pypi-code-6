"""
... module:: qsdn
    :platform: Unix, Windows
    :synopsis:  This module allows for parsing, validation and production of numeric literals, written with thousand separators through out the number.  Often underlying system libraries for working with locales neglect to put thousand separators (commas) after the decimal place or they sometimes use scientific notation.  The classes inherit from the Qt classes for making things less complex.
    
    Thousand separators in general will not always be commas but instead will be different according to the locale settings.  In Windows for example, the user can set his thousand separator to any character.  Support for converting strings directly to Decimals and from Decimals to strings is included.
    
    Also, numbers are always expressed in standard decimal notation.
        
    Care has been taken to overload all of the members in a way
    that is consistent with the base class QLocale and QValidator.  
"""

# Class inheritance diagram
#                      
#           [[QLocale]]
#                ^
#                |
#                |
#          [[QSDNLocale]]
#      

# Class inheritance diagram
#         
#         [[QValidator]]          
#                 ^               
#                 |               
#                 |               
#      [[QSDNNumericValidator]]
# 
# 
# SDN stands for 'standard decimal notation'.  That is not 'normalized Scientific notation'.

import decimal
from decimal import Decimal as D
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def add_commas(locale, st):
    if (locale.numberOptions() & QLocale.OmitGroupSeparator) != QLocale.OmitGroupSeparator:
    	dpl = (st.indexOf(locale.decimalPoint()) + st.length() + 1) % (st.length() + 1)
	i = dpl+4
	while i < st.length():
	    st.insert(i, locale.groupSeparator())
	    i += 4
	i = dpl-3
	while i > 0 and st[i] != ' ':
	    st.insert(i, locale.groupSeparator())	    
	    i -= 3
    return st



class QSDNLocale(QLocale) :
    """ 
        
    For a QSDNlocale, locale:  
        To get the Decimal of a string, s, use:
        
        (d, ok) = locale.toDecimal(s, 10)
        
        The value d is your decimal, and you should check ok before you trust d.
        
        To get the string representation use:
        
        s = locale.toString(d)
       
        
        
    """
    
    
    # p_mandatory_decimals becomes _mandatory_decimals
    # p_maximum_decimals becomes _maximum_decimals
    # they control the behavior of toString
    def __init__(self, _name = None, p_mandatory_decimals = D(0), p_maximum_decimals = decimal.Decimal('Infinity')) :
        """Control how many decimal places are put for units other than Decimal.
        
        Args:
          name (str) the name of the locale: example: "en_US"
        
          p_mandatory_decimals (int or Decimal) the mandatory decimal places required for a number
          
          p_maximum_decimals (int or Decimal) the maximum number of decimals required for a number
        """
        if _name.__class__ == str or _name.__class__ == QLocale or _name.__class__ == QSDNLocale:
                QLocale.__init__(self, _name)
        elif _name is None:
                    QLocale.__init__(self)
        else:
                    QLocale.__init__(self, _name)
        self._mandatory_decimals = p_mandatory_decimals
        self._maximum_decimals = p_maximum_decimals
            
            
    def toDecimal(self, s, base = 0):
    	"""This creates a decimal representation of s.
    	   
    	   It returns an ordered pair.  The first of the pair is the Decimal number, the second of the pair indicates whether the string had a valid representation of that number.  You should always check the second of the ordered pair before using the decimal returned.
    	   
    	   :note:
    	       Make sure you use 10 as the second argument or it may interpret the string as octal!
    	
           Like the other to* functions of QLocale as well as this class QSDNLocale, interpret a 
           a string and parse it and return a Decimal.  The base value is used to determine what base to use.
           
           If base is not set, numbers such as '0777' will be interpreted as octal.  The string '0x33' will
           be interpreted as hexadecimal and '777' will be interpreted as a decimal.  It is done this way
           so this works like toLong, toInt, toFloat, etc...
           Leading and trailing whitespace is ignored.
        """
        comma = self.groupSeparator()
        point = self.decimalPoint()
        if s.__class__ == QChar:
            code = s.digitValue()
            if code == -1 and base == 16:
                    code = QString(10*' '+'abcdef').indexOf(s, 10, Qt.CaseInsensitive)
            if  code != -1 and (base == 0 or code < base):
                    return (decimal.Decimal(code), True)
            return (decimal.Decimal('0'), False)
        # convert s, if it is a str, into a QString
        if s.__class__ == str:
            s = QString(s)
        # derive the base if not set above.
        try:
            # here a copy is made, the original s will not be
            # modified.
            s = s.trimmed()
            if base == 0:
                if s.startsWith('0x', Qt.CaseInsensitive):
                    s = s[2:]
                    base = 16
                elif s.startsWith('0'):
                    s = s[1:]
                    base = 8
                else:
                    base = 10
        except:
            return (0, False)
        v = decimal.Decimal("0")
        shift = decimal.Decimal('0')
        are_there_digits = False
        add_shifts = False
        comma_offset = None
        for c in s:
            if c == comma:
                if comma_offset == None:
                    comma_offset = 0
                elif comma_offset != 3:
                    return (1, False)
                elif self.numberOptions() & QLocale.RejectGroupSeparator == QLocale.RejectGroupSeparator:
                    return (2, False)
                comma_offset = 0
            elif c == point:
                comma_offset = 0
                if add_shifts:
                    # two decimal point characters is bad
                    return (v/base**shift, False)
                add_shifts = True
            else:
                to_add, status = self.toDecimal(QChar(c), base)
                if status:
                    are_there_digits = True
                    v *= base
                    v += to_add
                    if comma_offset != None:
                        comma_offset += 1
                    if add_shifts:
                        shift += 1
                else:
                    return (v / base**shift, False)
        v /= base ** shift
        return (v, are_there_digits)
    

    def toString(self, x, arg2 = None, arg3 = None):
    	"""    Convert any given Decimal, double, Date, Time, int or long to a string.
    
        Numbers are always converted to Standard decimal notation.  That is to say,
        numbers are never converted to scientifc notation.
        
        The way toString is controlled:
        If passing a decimal.Decimal typed value, the precision is recorded in the 
        number itself.  So, D('4.00') will be expressed as '4.00' and not '4'.
        D('4') will be expressed as '4'.
        
        When a number passed is NOT a Decimal, numbers are created in the following way:
        Two extra parameters, set during creation of the locale, determines how 
        many digits will appear in the result of toString().
        For example, we have a number like 5.1 and mandatory decimals was set    
        to 2, toString(5.1) should return '5.10'.  A number like 6 would be '6.00'.
        A number like 5.104 would depend on the maximum decimals setting, also 
        set at construction of the locale:
        _maximum_decimals controls the maximum number of decimals after the decimal point
        So, if _maximum_decimals is 6 and _mandatory_decimals is 2 then 
        toString(Decimal('3.1415929')) is '3.141,592'.
        Notice the number is truncated and not rounded.  
        Consider rounding a copy of the number before displaying.
        """
        	
        try:
            xt = D(x).as_tuple()
        except:
            return QLocale.toString(self, x, arg2, arg3)            
        digit_map = [(QString(QChar(a + self.zeroDigit().unicode()))) for a in range(0,10)]
        st = QString(  ''.join([unicode(digit_map[a]) for a in (xt.digits)])  )
        if -xt.exponent < st.length():
            # The decimal point must go to the right of the most significant digit.
            if xt.exponent < 0:                    
                # the decimal point goes next to a digit we already have
                st.insert(st.length()+xt.exponent, self.decimalPoint())
            else:
                # We need to add digits before we can write a decimal point
                # but if you don't have all of the digits for this.
                # Standard notation is always used here.
                # For example:
                # An expression like 3e2 becomes '300' even though, it is 
                # understood that such a value is not as precise as D(300). 
                st.append(digit_map[0].repeated(xt.exponent))                    
        else:
            # the digits all belong to places right of the decimal point. 
            st = (digit_map[0]) + QString(self.decimalPoint()) + (digit_map[0]).repeated(-xt.exponent-st.length()) + st
        dpl = st.indexOf(self.decimalPoint())
        if x.__class__ != D:
            if dpl == -1 and self._mandatory_decimals:
                st.append(self.decimalPoint() + digit_map[0].repeated(self._mandatory_decimals))
            if dpl != -1 and st.length() - dpl - 1 < self._mandatory_decimals:
                st.append(digit_map[0].repeated(self._mandatory_decimals - st.length() + dpl + 1))
            if dpl != -1 and st.length() - dpl - 1 > self._maximum_decimals:
                st.truncate(dpl+self._maximum_decimals+1)
            if dpl != -1:
                while st.endsWith(QString(self.zeroDigit())) and st.length()-dpl-1 > self._mandatory_decimals:
                    st.chop(1)
	st = add_commas(self, st)
        if xt.sign == 1:
            st.prepend(self.negativeSign())
        return st
                    
    @staticmethod                
    def system() :
    	""" Returns the system default for QSDNLocale.  
    	"""
        return QSDNLocale(QLocale.system())
    
    @staticmethod
    def c() :
    	""" Returns the C locale.  In the C locale, to* routines will not accept group separtors and do not produce them. 
    	"""
        _c = QSDNLocale()
        _c.setNumberOptions( QLocale.OmitGroupSeparator | QLocale.RejectGroupSeparator )
        return _c
        
            
    # returns a filtered copy of s so that it can be used by the  dumber QLocale's to* routines.
    #  if QLocale.RejectGroupSeparator is set, this routine wont filter commas.  A decimal point on the end of the number will be removed if 
    #  present.
    def _filtered(self, s):
        s = QString(s)
        if s.endsWith(QString(self.decimalPoint())):
            s.chop(1)
        if QLocale.RejectGroupSeparator & self.numberOptions() != QLocale.RejectGroupSeparator:
            s.remove(self.groupSeparator())
        return s
        
        
    # return a double represented by the string s.
    def toDouble(self, s):
            """ This creates a floating point representation of s.
    	   
    	    It returns an ordered pair.  The first of the pair is the number, the second of the pair indicates whether the string had a valid representation of that number.  You should always check the second of the ordered pair before using the number returned.
    	    """
            return QLocale.toDouble(self, self._filtered(s))
            
    # return a float represented by the string s.
    def toFloat(self, s):
            """ This creates a floating point representation of s.
    	   
    	    It returns an ordered pair.  The first of the pair is the number, the second of the pair indicates whether the string had a valid representation of that number.  You should always check the second of the ordered pair before using the number returned.
    	    """
            return QLocale.toFloat(self, self._filtered(s))
            
    # return a int represented by the string s.
    def toInt(self, s, base = 0):
        return QLocale.toInt(self, self._filtered(s), base)
   
    # return a long represented by the string s.
    def toLongLong(self, s, base = 0):
        """ This creates a numeric representation of s.
	    
        It returns an ordered pair.  The first of the pair is the number, the second of the pair indicates whether the string had a valid representation of that number.  You should always check the second of the ordered pair before using the number returned.
        
    	   :note:
    	       Make sure you use 10 as the second argument or it may interpret the string as octal!
    	
                               
        If base is not set, numbers such as '0777' will be interpreted as octal.  The string '0x33' will
        be interpreted as hexadecimal and '777' will be interpreted as a decimal.  It is done this way
        so this works like toLong, toInt, toFloat, etc...
        
        Leading and trailing whitespace is ignored.    	""" 
        return QLocale.toLongLong(self, self._filtered(s), base)
        
    def toShort(self, s, base = 0):
        """ This creates a numeric representation of s.
	    
        It returns an ordered pair.  The first of the pair is the number, the second of the pair indicates whether the string had a valid representation of that number.  You should always check the second of the ordered pair before using the number returned.
        
    	   :note:
    	       Make sure you use 10 as the second argument or it may interpret the string as octal!
    	
                               
        If base is not set, numbers such as '0777' will be interpreted as octal.  The string '0x33' will
        be interpreted as hexadecimal and '777' will be interpreted as a decimal.  It is done this way
        so this works like toLong, toInt, toFloat, etc...
        
        Leading and trailing whitespace is ignored.    	""" 
        return QLocale.toShort(self, self._filtered(s), base)
        
    # return a uint represented by the string s.
    def toUInt(self, s, base = 0):
        """ This creates a numeric representation of s.
	    
        It returns an ordered pair.  The first of the pair is the number, the second of the pair indicates whether the string had a valid representation of that number.  You should always check the second of the ordered pair before using the number returned.
        
    	   :note:
    	       Make sure you use 10 as the second argument or it may interpret the string as octal!
    	
                               
        If base is not set, numbers such as '0777' will be interpreted as octal.  The string '0x33' will
        be interpreted as hexadecimal and '777' will be interpreted as a decimal.  It is done this way
        so this works like toLong, toInt, toFloat, etc...
        
        Leading and trailing whitespace is ignored.    	""" 
        return QLocale.toUInt(self, self._filtered(s), base)

    # return a ulonglong represented by the string s.
    def toULongLong(self, s, base = 0):
        """ This creates a numeric representation of s.
	    
        It returns an ordered pair.  The first of the pair is the number, the second of the pair indicates whether the string had a valid representation of that number.  You should always check the second of the ordered pair before using the number returned.
        
    	   :note:
    	       Make sure you use 10 as the second argument or it may interpret the string as octal!
    	
                               
        If base is not set, numbers such as '0777' will be interpreted as octal.  The string '0x33' will
        be interpreted as hexadecimal and '777' will be interpreted as a decimal.  It is done this way
        so this works like toLong, toInt, toFloat, etc...
        
        Leading and trailing whitespace is ignored.    	""" 
        return QLocale.toULongLong(self, self._filtered(s), base)
        
    # return a ushort represented by the string s.
    def toUShort(self, s, base = 0):
        """ This creates a numeric representation of s.
	    
        It returns an ordered pair.  The first of the pair is the number, the second of the pair indicates whether the string had a valid representation of that number.  You should always check the second of the ordered pair before using the number returned.
        
    	   :note:
    	       Make sure you use 10 as the second argument or it may interpret the string as octal!
    	
                               
        If base is not set, numbers such as '0777' will be interpreted as octal.  The string '0x33' will
        be interpreted as hexadecimal and '777' will be interpreted as a decimal.  It is done this way
        so this works like toLong, toInt, toFloat, etc...
        
        Leading and trailing whitespace is ignored.    	""" 
        return QLocale.toUShort(self, self._filtered(s), base)

class QSDNNumericValidator(QValidator) :
    """ QSDNNumericValidator limits the number of digits after the decimal
     point and the number of digits before. 
     
      bitcoin                         :  QSDNNumericValidator(8, 8)
      US dollars less than $1,000,000 :  QSDNNumericValidator(6, 2)
      
      
      If use space is true, spaces are added on the left such that the location
      of decimal point remains constant.  Numbers like '10,000.004', '102.126' become 
      aligned.
      Bitcoin amounts:
      
                         '        0.004,3'
                         '       10.4'
                         '      320.0'
                         '        0.000,004'
                                                                                              
      U.S. dollar amounts;  
                         dollar = QSDNNumericValidator(6,2)
                         s = '42.1'
                         dollar.validate(s='42.1', 2)   =>  s = '     42.10'
                         s='50000'
                         dollar.toString(s)              => s = ' 50,000.00'
               
                                
    """                                                                                              
    def __init__(self, maximum_decamals = 1000, maximum_decimals = 1000, use_space = False, parent = None) :
        QValidator.__init__(self, parent)
        # true if we use spaces for justifying the string.
        self.spaced = use_space        
        self.characters_before_decimalPoint = maximum_decamals * 4 // 3
       	self.characters_after_decimalPoint = maximum_decimals * 4 // 3
        self._locale = QSDNLocale(QLocale.system())
        space_part = ' *' if self.spaced else ''
        decimalPoint = QRegExp.escape(QString(self._locale.decimalPoint()))
        groupSeparator = QRegExp.escape(QString(self._locale.groupSeparator()))
        self.proper_re = QRegExp('(' + space_part + \
            '\d{1,3}(' + groupSeparator + '\d{3})*)(' + decimalPoint + '((\d{3}' + groupSeparator + ')*\d{1,3})?)?')
        self.improper_decimal_re = QRegExp('(' + space_part + ')([\d' + groupSeparator + ']*)(' + decimalPoint + '([\d' + groupSeparator + ']*))?')
   
    def decimals(self):
    	""" gets the number of decimal points that are allowed *after* the decimal point """
	return self.characters_after_decimalPoint * 3//4
	
    def setDecimals(self, i):
    	""" sets the number of decimal digits that should be allowed **after** the decimal point """
	self.characters_after_decimalPoint = i * 4 // 3
	
    def decamals(self):
    	""" gets the number of decimal points that are allowed **before** the decimal point """
    	return self.characters_before_decimalPoint * 3 / 4
    	
    def setDecamals(self, i):
    	""" sets the number of decimal digits that should be allowed **before** the decimal point """
    	self.characters_before_decimalPoint = i * 4 // 3
    
    
    # Count non-space, non-comma characters: digits and a decimal point up to limit in QString s.    
    def _count_occurences(self, s, limit):
    	counter = 0
    	for i in range(0, limit):
    	    if s.at(i)  != QChar(self._locale.groupSeparator()) and s.at(i) != QChar(' '):
    	    	counter += 1
    	return counter;

    def _correct_white(self, s, pos):
	# Make it such that the number of characters before the decimal point is self.characters_before_decimalPoint by adding or removing spaces and returning a new position such that this new position will be between the same digits as the position indicated by pos.
	
    	whole_part = QRegExp(QString('^ *((\d|') + self._locale.groupSeparator() + ')*)')
    	whole_part.indexIn(s)    	
    	decimalPoint_location = whole_part.matchedLength()
    	assert(decimalPoint_location in range(0, s.length()+1))
    	needed_white = max(0, self.characters_before_decimalPoint - whole_part.cap(1).length())
	pos += self.characters_before_decimalPoint - decimalPoint_location if pos != 0 else 0
	s.replace( QRegExp("^ *"), QString(needed_white*' ') )
	assert(s.indexOf('.') == -1 or s.indexOf('.') == self.characters_before_decimalPoint)
	return pos
    	       	
    def validate(self, s, pos):
	""" Validates s, by adjusting the position of the commas to be in the correct places and adjusting pos accordingly as well as space in order to keep decimal points aligned when varying sized numbers are put one above the other.
	"""
	debug = False
    	if debug:
    	    print 'call to self.validate(%s,%d)' % (s,pos)
    	    print s
    	    print pos * ' ' + '^'
        if s.indexOf('!') != -1:
            self.emit(SIGNAL("bang()"))
            return QValidator.Invalid, pos
        if self.spaced:
            pos = self._correct_white(s, pos)
        if QRegExp("^ *").exactMatch(s):
            return QValidator.Intermediate, pos
        if not self.improper_decimal_re.exactMatch(s):
            return QValidator.Invalid, pos
	if self.proper_re.exactMatch(s):
	    # no need to fix the commas
	    whole_part = self.proper_re.cap(2)
	    fraction_part = self.proper_re.cap(3)
	    if fraction_part.__class__ != QString:
	    	fraction_part = QString("")
	    comma_last = False
	else:
	    pos_inside_spaces = pos < self.improper_decimal_re.pos(2)	    	     
	    comma_last = s.at(s.length()-1) == self._locale.groupSeparator()
	    after_comma = pos in range(1,s.length()+1) and s.at(pos-1) == self._locale.groupSeparator()
	    old_count = self._count_occurences(s, pos)
	    if debug:
		print 'digits before this position(%d) is %d' % (pos, old_count)
	    [whole_part, fraction_part] = [self.improper_decimal_re.cap(2), self.improper_decimal_re.cap(4)]
	    whole_part.replace(QString(self._locale.groupSeparator()), '')
	    fraction_part.replace(QString(self._locale.groupSeparator()),'')
	    fraction_part = add_commas( self._locale, QString(str(fraction_part)[::-1]) )
	    fraction_part = QString(str(fraction_part)[::-1])
	    if fraction_part != QString(''):
	    	fraction_part.prepend(self._locale.decimalPoint())
            whole_part = add_commas(self._locale, whole_part) if whole_part != '' else QString('0')
	    s.clear()
	    s.append(self.improper_decimal_re.cap(1)) # the spaces
	    s.append(whole_part)
	    s.append(fraction_part)
	    if comma_last:
		s.append(',')
	    pos = max(0, self.improper_decimal_re.pos(1)) if pos_inside_spaces else max(0, self.improper_decimal_re.pos(2))
	    while pos < s.length() and old_count > 0:
		if s[pos] != self._locale.groupSeparator() and s.at(pos) != QChar(' '):
		    old_count -= 1
		if debug:
		    print "(%d,%d)" % (old_count, pos)
		pos += 1
	    if debug:
		print 'digits before this position(%d) is %d' % (pos, self._count_occurences(s, pos))
	    if after_comma and pos in range(0,s.length()) and s[pos] == self._locale.groupSeparator():
		pos += 1
	    if debug:
		print 'new position is %d' % pos
	    if self.spaced:
		pos = self._correct_white(s, pos)
	    if debug:
		print 'digits before this position(%d) is %d' % (pos, self._count_occurences(s, pos))
		print s
		print pos * ' ' + '^'
		print 'exiting'
        if fraction_part.length() > self.characters_after_decimalPoint+1:
            s.truncate(s.length()-1)
	if comma_last or whole_part.length() > self.characters_before_decimalPoint or fraction_part.length() > 1+self.characters_after_decimalPoint:
	    return QValidator.Intermediate, pos
	else:
	    return QValidator.Acceptable, pos

    def setLocale(self, plocale):
    	""" Set the locale used by this Validator.  
    	"""
    	self._locale = plocale
    	self.emit(SIGNAL("localeSet"), plocale)

    def locale(self):
    	""" get the locale used by this validator 
    	"""
    	return self._locale
