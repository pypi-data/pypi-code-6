# -*- coding: iso-8859-1 -*-
# MARDS\standard_types.py
#
# INTERNAL SUPPORT FOR STANDARD TYPES
#

from rolne import rolne
import regex
import decimal
import math
from mards_library import SCHEMA_to_rolne, schema_match_up
from standard_types_schema import standard_types_text


standard_type_rolne, e = SCHEMA_to_rolne(standard_types_text)
if e:
    print "standard_library errors: "+repr(e)
    
def apply_schema_types(doc, schema):
    global standard_type_rolne
    copy = schema.copy(seq_prefix="", seq_suffix="")
    copy.extend(standard_type_rolne, prefix="std_type.")
    return _apply_schema_types(doc, schema, copy)

def _apply_schema_types(doc, orig_schema, extended):
    schema = schema_match_up(doc, orig_schema)
    error_list = []
    to_delete = []
    for item in doc:
        rule = get_item_rule(item, schema)
        if rule:
            if rule.find("value"):
                if rule.find("value").list_names("type"):
                    e = do_normalization(item, rule["value"]["type"], extended)
                    if e:
                        error_list.extend(e)
                        for err in e:
                            if err[0]=="[error]":
                                to_delete.append(item.seq)
                                break
            if len(item):
                el = _apply_schema_types(item, rule, extended)
                error_list += el
    for seq in to_delete:
        doc.seq_delete(seq)
    return error_list
    
def get_item_rule(item, schema):
    if item.name in schema.list_values("name"):
        return schema["name", item.name]
    return None    
    
def do_normalization(item, rule, schema):
    value_type = rule.value
    type_rule = schema.find("define_type", value_type)
    error_list = []
    if  value_type=="string":
        pass ## nothing to do for a string type
    elif value_type=="label":
        error_list = do_norm_label(item, rule, type_rule)
    elif value_type=="price":
        error_list = do_norm_price(item, rule, type_rule)
    elif value_type=="qty":
        error_list = do_norm_qty(item, rule, type_rule)
    elif value_type=="percent":
        error_list = do_norm_percent(item, rule, type_rule)
    elif value_type=="check_list":
        error_list = do_norm_check_list(item, rule, type_rule)
    elif value_type=="radio_select":
        error_list = do_norm_radio_select(item, rule, type_rule)
    elif value_type=="ignore":
        item.value = None
    elif value_type=="unit":
        pass ## nothing to do for a unit type
    elif value_type=="angle":
        error_list = do_norm_angle(item, rule, type_rule)
    elif value_type=="file":
        pass  
    elif value_type=="length":
        error_list = do_norm_length(item, rule, type_rule)
    elif value_type=="distance":
        type_rule = schema.find("define_type", "length")
        error_list = do_norm_length(item, rule, type_rule, as_distance=True)
    elif value_type=="duration":
        error_list = do_norm_duration(item, rule, type_rule)
    elif value_type=="mass":
        error_list = do_norm_mass(item, rule, type_rule)
    elif value_type=="temperature":
        error_list = do_norm_temperature(item, rule, type_rule)
    elif value_type=="luminous_intensity":
        error_list = do_norm_luminous_intensity(item, rule, type_rule)
    elif value_type=="current":
        error_list = do_norm_current(item, rule, type_rule)
    elif value_type=="voltage":
        error_list = do_norm_voltage(item, rule, type_rule)
    elif value_type=="frequency":
        error_list = do_norm_frequency(item, rule, type_rule)
    elif value_type=="boolean":
        error_list = do_norm_boolean(item, rule, type_rule)
    elif value_type=="integer":
        error_list = do_norm_integer(item, rule, type_rule)
    elif value_type=="float":
        error_list = do_norm_float(item, rule, type_rule)
    elif value_type=="hexadecimal":
        error_list = do_norm_hexadecimal(item, rule, type_rule)
    else:
        # TODO: allow/search for user-defined types
        if type_rule is not None:
            pass ## nothing to do as it is user defined
        else:
            error_list = [ ("[error]", "schema", rule.seq, "'type {}' unknown.".format(value_type)) ]
    return error_list
    
def rst(value_rule):
    '''Given the data and type information, generate a list of strings for
    insertion into a RST document.
    '''
    lines = []
    if value_rule.has('type'):
        value_type = value_rule['type'].value
    else:
        value_type = 'string'
    if value_type=='ignore':
        pass
    else:
        lines.append('A *'+value_type+'* value is expected.')
        lines.append('')
    if value_type=="string":
        pass
    elif value_type=="label":
        pass
    elif value_type=="price":
        pass
    elif value_type=="qty":
        pass
    elif value_type=="percent":
        pass
    elif value_type=="check_list":
        pass
    elif value_type=="radio_select":
        pass
    elif value_type=="ignore":
        pass
    elif value_type=="unit":
        pass
    elif value_type=="angle":
        pass
    elif value_type=="file":
        pass
    elif value_type=="length":
        pass
    elif value_type=="distance":
        pass
    elif value_type=="duration":
        pass
    elif value_type=="mass":
        pass
    elif value_type=="temperature":
        pass
    elif value_type=="luminous_intensity":
        pass
    elif value_type=="current":
        pass
    elif value_type=="voltage":
        pass
    elif value_type=="frequency":
        pass
    elif value_type=="boolean":
        pass
    elif value_type=="integer":
        pass
    elif value_type=="float":
        pass
    elif value_type=="hexadecimal":
        pass
    return lines
    
label_search = regex.compile(ur"[\p{Z}\p{P}^](?<!_)(?<!\.)(?<!\*)", regex.UNICODE)

def do_norm_label(item, rule, type_rule):
    global label_search
    error_list = []
    value = unicode(item.value)
    #TODO check for required?
    if value is not None:
        r = label_search.search(value)
        if r:
            error_list = [("[error]", "doc", item.seq, "'{} {}' has characters not permitted. Detail: '{}'".format(item.name, value, str(r)))]
    return error_list

def do_norm_price(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value, strip_list=['$'])
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a price.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if unit == "USD":
            final = number*decimal.Decimal('1.00')
        elif unit == "USD_cents":
            final = number/decimal.Decimal('100.00')
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a currency (price) unit.".format(raw_unit))]
            return error_list
        else:
            final = number*decimal.Decimal('1.00')
        final = final.quantize(decimal.Decimal('0.000001'))
        string = str(final)+" USD"
        item.value = string
    return error_list

def do_norm_qty(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a quantity.".format(str(item.value)))]
    else:
        if raw_unit:
            error_list = [("[error]", "doc", item.seq, "a unit '{}' is not expected for a basic quantity.".format(raw_unit))]
            return error_list
        else:
            final = number
        before = str(final)
        final = final.quantize(decimal.Decimal('1'))
        string = str(final)
        if string!=before:
            error_list = [("[warning]", "doc", item.seq, "'{}' was rounded to '{}' as a basic quantity.".format(before, string))]
        item.value = string
    return error_list

def do_norm_percent(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a percentage.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if unit == "fraction":
            final = number*decimal.Decimal('100')
        elif unit == "percent":
            final = number
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a percent symbol or unit.".format(raw_unit))]
            return error_list
        else:
            final = number
        string = str(final) + " %"
        item.value = string
    return error_list
    
def do_norm_check_list(item, rule, type_rule):
    global label_search
    error_list = []
    label_list = []
    in_word_state = False
    for ch in item.value:
        if in_word_state:
            if label_search.search(ch):
                in_word_state = False
                label_list.append(new_word)
                new_word = ""
            else:
                new_word += ch
        else:
            if label_search.search(ch):
                pass
            else:
                new_word = ch
                in_word_state = True
    else:
        if new_word:
            label_list.append(new_word)
    proper_labels = rule.list_values("choice")
    final_list = []
    for label in label_list:
        if label in proper_labels:
            final_list.append(label)
        else:
            error_list.append( ("[error]", "doc", item.seq, "item '{}' not found in allowed choices: {}. item ignored.".format(label, repr(proper_labels))) )
    string = ", ".join(final_list)
    item.value = string
    return error_list

def do_norm_radio_select(item, rule, type_rule):
    global label_search
    error_list = []
    if item.value is not None:
        value = unicode(item.value)
        proper_labels = rule.list_values("choice")
        if value not in proper_labels:
            error_list.append( ("[error]", "doc", item.seq, "selection '{}' not found in allowed choices: {}.".format(value, repr(proper_labels))) )
    return error_list

def do_norm_angle(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as an angle.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if unit == "degree":
            final = math.radians(number)
        elif unit == "radian":
            final = number
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a percent symbol or unit.".format(raw_unit))]
            return error_list
        else:
            final = number
        string = str(final) + " radians"
        item.value = string
    return error_list
   
def do_norm_length(item, rule, type_rule, as_distance=False):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        if as_distance:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a distance.".format(str(item.value)))]
        else:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a length.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if (unit == "in"):
            final = number*decimal.Decimal('0.0254')
        elif (unit == "ft"):
            final = number*decimal.Decimal('0.3048')
        elif (unit == "yd"):
            final = number*decimal.Decimal('0.9114')
        elif (unit=="mi"):
            final = number*decimal.Decimal('1609.34')
        elif (unit == "km"):
            final = number*decimal.Decimal('1000')
        elif unit == "hm":
            final = number*decimal.Decimal('100')
        elif unit == "dam":
            final = number*decimal.Decimal('10')
        elif (unit == "m"):
            final = number
        elif unit == "dm":
            final = number*decimal.Decimal('0.1')
        elif unit == "cm":
            final = number*decimal.Decimal('0.01')
        elif unit == "mm":
            final = number*decimal.Decimal('0.001')
        elif unit == False:
            if as_distance:
                error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a distance unit.".format(raw_unit))]
            else:
                error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a length unit.".format(raw_unit))]
            return error_list
        else:
            final = number
        if as_distance and final<0:
            final = final*decimal.Decimal('-1')
        string = str(final)+" m"
        item.value = string
    return error_list

def do_norm_duration(item, rule, type_rule):
    error_list = []
    if item.value is None:
        return error_list
    string = item.value
    success = True
    if ":" in string:
        ###
        #  handle a string in hours:min:sec format
        ###
        parts = string.split(":")
        mult = decimal.Decimal('1')
        number = decimal.Decimal('0.0')
        for part in reversed(parts):
            try:
                temp = decimal.Decimal(part.strip())
                number += temp*mult
            except:
                success = False
                error_list.append(  ("[error]", "doc", item.seq, "unable to interpret '{}' as a portion of time.".format(part))  )
            mult = mult*decimal.Decimal('60')
    else:
        ###
        #  handle a wild string
        #    possiblities:
        #     simple:  24 sec
        #     pairs: 1 minute 22 sec
        #     trunc pairs: 1 minute 22
        #     mushed pairs: 1minute 22sec
        #     out of order mushed:  22sec 1minute
        #     bunch of seconds: 2 3 6
        #           (2+3+6 = 11s)
        ###
        pair_list = []
        word_list = string.split()
        pending_number = None
        for word in word_list:
            good_number_flag, number, raw_unit = split_number_unit(word)
            if good_number_flag and raw_unit:
                if pending_number:
                    pair_list.append( (pending_number, "s") )
                pair_list.append( (number, raw_unit) )
                pending_number = None
            elif good_number_flag:
                if pending_number:
                    pair_list.append( (pending_number, "s") )
                pending_number = number
            else:
                if raw_unit.lower() in ["and", "+", "&"]:
                    continue
                if pending_number:
                    pair_list.append( (pending_number, raw_unit) )
                    pending_number = None
                else:
                    error_list.append(("[error]", "doc", item.seq, "unable to interpret '{}' duration. note: '{}' in context.".format(string, word)))
                    success = False
        else:
            if pending_number:
                pair_list.append( (pending_number, "s") )
        number = decimal.Decimal()
        for (num_part, raw_unit) in pair_list:
            unit = find_unit(raw_unit.lower(), type_rule)
            if (unit == "s"):
                number += num_part
            elif (unit == "m"):
                number += num_part*decimal.Decimal('60')
            elif (unit == "h"):
                number += num_part*decimal.Decimal(60*60)
            elif (unit=="d"):
                number += num_part*decimal.Decimal(60*60*24)
            elif unit == False:
                error_list.append(("[error]", "doc", item.seq, "unable to interpret '{} {}' as a time unit for duration.".format(str(num_part), raw_unit)))
                success = False
    if success:
        final = str(number)+" s"
        item.value = final
    return error_list

def do_norm_mass(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a mass.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if raw_unit == "mg": # resolving capitalization difference
            unit = "mg"
        if raw_unit == "Mg": # resolving capitalization difference
            unit = "tonne"
        if unit == "kg":
            final = number
        elif unit == "hg":
            final = number/decimal.Decimal('10')           
        elif unit == "dag":
            final = number/decimal.Decimal('100')           
        elif unit == "g":
            final = number/decimal.Decimal('1000')
        elif unit == "dg":
            final = number/decimal.Decimal('10000')
        elif unit == "cg":
            final = number/decimal.Decimal('100000')
        elif unit == "mg":
            final = number/decimal.Decimal('1000000')
        elif unit == "mcg":
            final = number/decimal.Decimal('1000000000')
        elif unit == "tonne":
            final = number*decimal.Decimal('1000')
        elif unit == "long":
            final = number*decimal.Decimal('1016.05')
        elif unit == "short":
            final = number*decimal.Decimal('907.185')
        elif unit == "slug":
            final = number*decimal.Decimal('14.9539029')
        elif unit == "stone":
            final = number*decimal.Decimal('6.35029')
        elif unit == "lb":
            final = number*decimal.Decimal('0.453592')
        elif unit == "oz":
            final = number*decimal.Decimal('0.0283495')
        elif unit == "troy":
            final = number*decimal.Decimal('0.0311034768')
        elif unit == "grain":
            final = number*decimal.Decimal('6.479891E-5')
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a unit of mass.".format(raw_unit))]
            return error_list
        else:
            final = number
        string = str(final) + " kg"
        item.value = string
    return error_list
    
def do_norm_temperature(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a temperature.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if unit == "k":
            final = number
        elif unit == "f":
            decimal.getcontext().prec = 6
            final = decimal.Decimal(5.0/9.0)*( number+decimal.Decimal('459.67') )
            decimal.getcontext().prec = 28
        elif unit == "c":
            final = number + decimal.Decimal('273.15')           
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a unit of temperature.".format(raw_unit))]
            return error_list
        else:
            final = number
        string = str(final) + " K"
        item.value = string
    return error_list

def do_norm_luminous_intensity(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a luminous intensity.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if unit == "cd":
            final = number
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a unit of luminous intensity.".format(raw_unit))]
            return error_list
        else:
            final = number
        string = str(final) + " cd"
        item.value = string
    return error_list

def do_norm_current(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as an electrical current value.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if unit == "a":
            final = number
        elif unit == "ma":
            final = number/decimal.Decimal('1000')           
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a unit of electrical current.".format(raw_unit))]
            return error_list
        else:
            final = number
        string = str(final) + " A"
        item.value = string
    return error_list
    
def do_norm_voltage(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a voltage level.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if raw_unit.lower()=="mv":
            unit = "millivolt"
        if raw_unit=="MV":
            unit = "megavolt"
        if unit == "v":
            final = number
        elif unit == "microvolt":
            final = number/decimal.Decimal('1000000')           
        elif unit == "millivolt":
            final = number/decimal.Decimal('1000')           
        elif unit == "kilovolt":
            final = number*decimal.Decimal('1000')           
        elif unit == "megavolt":
            final = number*decimal.Decimal('1000000')           
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a unit of voltage.".format(raw_unit))]
            return error_list
        else:
            final = number
        string = str(final) + " V"
        item.value = string
    return error_list

def do_norm_frequency(item, rule, type_rule):
    error_list = []
    flag, number, raw_unit = split_number_unit(item.value)
    if not flag:
        error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as an frequency value.".format(str(item.value)))]
    else:
        unit = find_unit(raw_unit.lower(), type_rule)
        if unit == "hz":
            final = number
        elif unit == "khz":
            final = number*decimal.Decimal('1000')           
        elif unit == "mhz":
            final = number*decimal.Decimal('1000000')           
        elif unit == "ghz":
            final = number*decimal.Decimal('1000000000')           
        elif unit == "invert_s":
            if number!=0:
                final = decimal.Decimal(1.0)/number           
            else:
                error_list = [("[error]", "doc", item.seq, "error: a frequency with a period of zero (0) is infinite.".format(raw_unit))]
                return error_list
        elif unit == "invert_ms":
            if number!=0:
                final = decimal.Decimal(1000.0)/number           
            else:
                error_list = [("[error]", "doc", item.seq, "error: a frequency with a period of zero (0) is infinite.".format(raw_unit))]
                return error_list
        elif unit==False:
            error_list = [("[error]", "doc", item.seq, "unable to interpret '{}' as a unit of frequency.".format(raw_unit))]
            return error_list
        else:
            final = number
        string = str(final) + " Hz"
        item.value = string
    return error_list

def do_norm_boolean(item, rule, type_rule):
    error_list = []
    result = None
    if item.value is not None:
        value = unicode(item.value.lower())
        true_words = type_rule["unit", "true"].list_values("*")
        false_words = type_rule["unit", "false"].list_values("*")
        if value in true_words:
            result = "true"
        elif value in false_words:
            result = "false"
        else:
            error_list.append( ("[error]", "doc", item.seq, "unable to determine if '{}' is true or false.".format(item.value)) )
    if result:
        item.value = result
    return error_list

def do_norm_integer(item, rule, type_rule):
    error_list = []
    result = None
    if item.value is not None:
        value = item.value.strip()
        try:
            number = decimal.Decimal(value)
            if "." in str(number):
                number = number.quantize(decimal.Decimal('1'))
                error_list.append( ("[warning]", "doc", item.seq, "trimming off fractional part of number.".format(item.value)) )
            item.value = str(number)
        except Exception, e:
            error_list.append( ("[error]", "doc", item.seq, "unable to convert '{}' into an integer. msg: {}".format(item.value, str(e))) )
    return error_list

def do_norm_float(item, rule, type_rule):
    error_list = []
    result = None
    if item.value is not None:
        value = item.value.strip()
        try:
            number = decimal.Decimal(value)
            string = sci_str(number)
            item.value = string
        except Exception, e:
            error_list.append( ("[error]", "doc", item.seq, "unable to convert '{}' into a floating point number. msg: {}".format(item.value, str(e))) )
    return error_list

def do_norm_hexadecimal(item, rule, type_rule):
    error_list = []
    string = str(item.value).lower()
    if item.value is not None:
        bad_chars = ""
        final = ""
        for ch in string:
            if ch in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']:
                final += ch
            else:
                bad_chars += ch
        if bad_chars:
            error_list = [("[warning]", "doc", item.seq, "'{} {}' has characters not permitted: '{}'".format(item.name, item.value, ", ".join(bad_chars)))]
        item.value = final
    return error_list

def sci_str(dec):
    return ('{:.' + str(len(dec.as_tuple().digits) - 1) + 'e}').format(dec)
    
def find_unit(target, rule):
    if not target:
        return None
    for unit_label in rule.list_values("unit"):
        if target in rule["unit", unit_label].list_values("*"):
            return unit_label
    return False
    
def split_number_unit(string, strip_list=None):
    ''' 
        takes a string and grabs the leading number and the following unit 
        both the number and unit returned are simple strings
        returns a triple tuple of (successFlag, number, unit)
        successFlag is False if the number is invalid
    '''
    successFlag = True
    state = 0
    number_so_far = ""
    unit_so_far = ""
    decimal_found = False
    negate_flag = False
    if string is None:
        return (False, "", "")
    string = string.strip()
    if not strip_list:
        strip_list = []
    if len(string):
        if string[0]=="-":
            negate_flag = True
            string = string[1:]
    if len(string):
        if string[0]==".":
            string = "0"+string  # a string of ".12" is actually a legit number, but the lack of a preceding 0 will confuse python, so we tack on a zero
    if len(string):
        for char in string:
            if state==0:  # number state
                if char in ['0','1','2','3','4','5','6','7','8','9']:
                    number_so_far += char
                elif char in strip_list:
                    pass
                elif char==".":
                    if decimal_found:
                        successFlag = False # units do not begin with a period. ex: 234.2.anything 
                        state=2
                    else:
                        number_so_far += char
                        decimal_found = True
                elif char=="\n":
                    state=2
                else:
                    unit_so_far += char
                    state=1
            elif state==1: # unit state
                if char=="\n":
                    state=2
                elif char in strip_list:
                    pass
                else:
                    unit_so_far += char
            else: # discard state
                pass
        # clean up 
        unit_so_far = unit_so_far.strip()
        if len(number_so_far)==0:
            successFlag = False
        if negate_flag:
            number_so_far = "-"+number_so_far
        try:
            number_so_far = decimal.Decimal(number_so_far)
        except:
            successFlag = False
    else:
        successFlag = False
    if not successFlag:
        return(successFlag, "", unit_so_far)
    return (successFlag, number_so_far, unit_so_far)
