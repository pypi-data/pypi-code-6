# -*- coding: iso-8859-1 -*-
# MARDS\standard_types_schema.py
#
# THE STANDARD TYPES SCHEMA DOCUMENT
#

standard_types_text = '''\
define_type string
    describe en
        title "String (UTF8)"
        body "A string is any sequence of UTF8 characters. This is the default type if no other type is specified."

define_type label
    describe en
        title "Label"
        body "A UTF8 unicode string containing alphabetic characters, digits 0 to 9, underscores (\_), and periods. No other characters are permitted. Labels are generally case-sensitive."
        body ""
        body "Very explicitly: whitespace characters are forbidden (such as SPACE and TAB). Punctuation of any kind (other than underscores and periods) are forbidden."
        body ""
        body "The MARDS spec uses label rules for names in the name<space>value. However, it purposefully makes exception for labels that start with # symbol for outside-context exceptions such as for comments."
        body ""
        body "#Convention"
        body ""
        body "A label that follows the rules is ultimates a true label. However, there are conventions used in the making of the labels in English. Following these conventions makes the human interpretation of the labels much easier. They are as follows:"
        body ""
        body " *  Seperate words with underscores. Don't use CamelCase. So, instead of:"
        body ""
        body "    `OneTwoThree`"
        body ""
        body "    use:"
        body ""
        body "    `one_two_three`"
        body ""
        body " *  use all lower case letters unless called for by standard writing convention. A label is not assumed to be a sentence, so the first word should not be capitalized unless called for by other convention rules. So, instead of:"
        body ""
        body "    `Qty_Of_Johns_Boxes`"
        body ""
        body "    use:"
        body ""
        body "    `qty_of_Johns_boxes`"
        body ""
        body "    Notice that 'J' remains capitalized since 'John' is a persons name and would be capitalized by English writing convention."
        body ""
        body " *  Punctuation is 'skipped' rather than given an underscore unless such an underscore greatly adds clarity. So, instead of:"
        body ""
        body "    `qty_of_John_s_boxes`"
        body ""
        body "    use:"
        body ""
        body "    `qty_of_Johns_boxes`"
        body ""
        body " *  if the label is a schema name, imply the type of unit expected IF it aids clarity. Ideally it would be a suffix with the full type label. So, instead of:"
        body ""
        body "    `part4_twist`"
        body ""
        body "    use:"
        body ""
        body "    `part4_twist_percent`"
        body ""
        body " *  avoid the use of periods (.) for simple labels. The periods are meant to imply sectional seperation. TODO: expand this."
        body " *  reserve labels that start with an underscore for information that should be repressed from publication or normal/typical view. A single underscore implies mild suppression. A double underscore implies strong supression. The actual meaning of 'suppression' is a matter of context."
        body " *  Don't end a label with underscores or periods."

define_type price
    describe en
        title "Price"
        body "The proposed quantity of money or other compensation in exchange for a good or service. The normalization depends on the currency."
    unit USD
        describe en
            title "U.S. Dollars"
            body "A quantity of US Dollars. Precision is assumed to be to 6 decimal places. That is to say that $43.1234567 would be rounded to `43.123457 USD`. Regardless of the number, at least two decimal places are displayed. For example, $100 would normalize to `100.00 USD` but $100.932 would normalize to `100.932 USD`. But, again, the precision is to 6 decimal places regardless of display. So, $100.000000 is the same as $100. And, $100.932 is the same as $100.932000.
        default
        * "usd"
        * "us"
        * "dollars"
        ## prefix "$"
    unit USD_cents
        * "c"
        * "cents"
        * "pennies"
        * "¢"

define_type qty
    describe en
        title "Quantity"
        body "A positive integer representing the amount of discrete objects, items, or services contained, needed, or desired. The number range is from 0 to 9223372036854775807. Normalized to a series of decimal digits with no seperators."

define_type percent
    describe en
        title "Percentage"
        body "A fraction of unity. Normalized to a simple decimal percentage. So, nothing is '0.0' and all is '1.0'. Can alternatively represented by the '%' symbol, such as '0%' and '100%'."
    unit fraction
        * "of"
        * "frac"
        * "fraction"
        * "parts"
    unit percent
        default
        * "%"
        * "perc"
        * "percent"

define_type check_list
    describe en
        title "Choice/Check List"
        body "A list of labels. Each label is restricted to the 'choice' elements under the 'type check_list' definition."
        body ""
        body "Each label is seperated by whitespace and/or other non-label characters."
        body ""
        body "A common convention is to use commas to visually aid in the seperation. This is not strictly required however. So, a value of `one, two, three` is the same as `one two three`. The single COMMA SPACE seperation is the normalized result."
        body ""
        body "If the schema defines the value as _required_, then the there must be at least one label selected. Otherwise, zero labels can be selected."
    name choice
        treatment unique
        value
            required
            type label

define_type radio_select
    describe en
        title "Radio Select"
        body "A selected string. The string is restricted to the 'choice' elements under the 'type radio_select' definition."
        body ""
        body "If the schema defines the value as _required_, then the there must be a string selected. Otherwise, the value can be empty."
    name choice
        treatment unique
        value
            required
            type string

define_type ignore
    describe en
        title "Ignored Value"
        body "A value with an 'ignore' type is discarded. Normalized to an empty string."

define_type unit
    describe en
        title "Desired Unit"
        body "A short sequence of characters indicating a desired or required unit of measurement. It is treated just like a 'string' type. It's actual interpretation depends on the application."

define_type angle
    describe en
        body "A measure of rotation (or arc) about a common vertex. It is normalized to simple radians."
    unit degree
        * "°"
        * "@deg;"
        * "&#176;"
        * "deg"
        * "degree"
    unit radian
        default
        * "rad"
        * "radian"

define_type file
    describe en
        title "File name"
        body "A name of a file on an storage system."

define_type length
    describe en
        title "Length"
        body "The extent of something from end to end. Normalized to SI unit of meter (m)"
    unit m
        default
        * "m"
        * "meter"
        * "meters"
        * "metre"
        * "metres"
    unit mm
        * "mm"
        * "millimeter"
        * "millimeters"
        * "millimetre"
        * "millimetres"
    unit cm
        * "cm"
        * "centimeter"
        * "centimeters"
        * "centimetre"
        * "centimetres"
    unit dm
        * "dm"
        * "decimeter"
        * "decimeters"
        * "decimetre"
        * "decimetres"
    unit km
        * "k"
        * "km"
        * "kilometer"
        * "kilometers"
        * "kilometre"
        * "kilometres"
    unit mi
        * "mi"
        * "mile"
        * "miles"
    unit in
        * "i"
        * "in"
        * "inch"
        * "inches"
    unit ft
        * "f"
        * "ft"
        * "feet"
    unit yd
        * "y"
        * "yd"
        * "yard"
        * "yards"
        
define_type distance
    describe en
        title "Distance"
        body "A positive numeric measure of the how far apart two objects are. Normalized to the SI unit of meter (m). If the value is found to be negative, it is made positive."
        
define_type duration
    describe en
        title "Duration"
        body "A positive measure of time between two events. Normalized to SI unit of seconds (s)."
    unit s
        default
        * "s"
        * "sec"
        * "second"
        * "seconds"
    unit m
        * "m"
        * "min"
        * "mins"
        * "minute"
        * "minutes"
    unit h
        * "h"
        * "hr"
        * "hrs"
        * "hour"
        * "hours"
    unit d
        * "d"
        * "day"
        * "days"

define_type mass
    describe en
        title "Mass"
        body "A positive measure of the physical property of a bodies resistence to accelleration by force. At rest on a planet, weight and mass are commonly the same thing. Normalized to the SI unit of kilograme (kg)."
    unit g
        * "g"
        * "gr"
        * "gram"
        * "grams"
    unit kg
        default
        * "kg"
        * "k"
        * "kilo"
        * "kilogram"
        * "kilograms"
        * "kilograme"
        * "kilogrames"
    unit hg
        * "hg"
    unit dag
        * "dag"
    unit dg
        * "dg"
    unit cg
        * "cg"
    unit mg
        * "mg"
        ## repeat
    unit mcg
        * "mcg"
    unit tonne
        * "t"
        * "tonne"
        * "tonnes"
        * "metric ton"
        * "metric tons"
        * "mg"
        ## repeat
    unit long
        * "lt"
        * "long ton"
        * "long tons"
    unit short
        * "st"
        * "short ton"
        * "short tons"
    unit slug
        * "sl"
        * "slug"
    unit stone
        * "stone"
    unit lb
        * "lb"
        * "lbs"
        * "pound"
        * "pounds"
    unit oz
        * "oz"
        * "ounce"
        * "ounces"
    unit troy
        * "oz t"
        * "troy"
        * "troy oz"
        * "troy ounce"
        * "troy ounces"
    unit grain
        * "grain"
        
define_type temperature
    describe en
        title "Temperature"
        body "A measure of hot and cold. Normalized to the SI unit of the Kelvin (K)".
    unit f
        * "f"
        * "°f"
        * "fahrenheit"
    unit c
        * "c"
        * "°c"
        * "celcius"
    unit k
        default
        * "k"
        * "°k"
        * "kelvin"
        
define_type luminous_intensity
    describe en
        title "Luminous Intensity"
        body "A measure of the vavelength-weighted power emitted by a light source in a particular direction per unit solid angle (see wikipedia). Normalized to the SI unit of candela (cd)."
    unit cd
        default
        * "cd"
        * "candela"

define_type current
    describe en
        title "Electrical Current"
        body "The flow of electric charge. Normalized to the SI unit of ampere (A)."
    unit a
        default
        * "a"
        * "amp"
        * "amps"
        * "ampere"
        * "amperes"
    unit ma
        * "ma"
        * "milliamp"
        * "milliamps"
        
define_type voltage
    describe en
        title "Electrical Voltage"
        body "The potential of electric force. Normalized to the SI unit of volt (V)."
    unit v
        default
        * "v"
        * "volt"
        * "volts"
    unit microvolt
        * "microvolt"
        * "microvolts"
        * "µv"
    unit millivolt
        * "millivolt"
        * "millivolts"
        * "mv"
        ## repeat
    unit kilovolt
        * "kilovolt"
        * "kilovolts"
        * "kv"
    unit megavolt
        * "megavolt"
        * "megavolts"
        * "mv"
        ## repeat
        
define_type frequency
    describe en
        title "Frequency"
        body "The count of events per unit of time. Normalized to the SI unit of hertz (Hz)."
    unit hz
        default
        * "hz"
        * "hertz"
        * "per second"
        * "/s"
        * "/ s"
    unit khz
        * "khz"
    unit mhz
        * "mhz"
    unit ghz
        * "ghz"
    unit invert_s
        * "s"
        * "seconds"
    unit invert_ms
        * "ms"
        * "milliseconds"

define_type boolean
    describe en
        title "Boolean"
        body "The state of either Truth (existence) or False (non-existence). Normalized to the interpretation JSON-like 'true' for true and 'false' for false."
    unit true
        default
        * "true"
        * 1
        * -1
        * "good"
        * "t"
        * "correct"
        * "yes"
        * "one"
        * "yep"
        * "pass"
        * "passed"
        * "accept"
        * "accepted"
        * "consent"
        * "consented"
        * "agree"
        * "agreed"
        * "embrace"
        * "cherish"
        * "exalt"
        * "love"
        * "submit"
        * "enfold"
        * "include"
        * "bless"
        * "blessed"
        * "clean"
    unit false
        * "false"
        * 0
        * "bad"
        * "f"
        * "incorrect"
        * "no"
        * "0"
        * "zero"
        * "nope"
        * "fail"
        * "failed"
        * "reject"
        * "rejected"
        * "deny"
        * "denied"
        * "decline"
        * "declined"
        * "evil"
        * "hate"
        * "hated"
        * "decry"
        * "decried"
        * "exclude"
        * "debase"
        * "debased"
        * "imprecate"
        * "curse"
        * "cursed"
        * "impure"

define_type integer
    describe en
        title "Integer (Whole Number)"
        body "A non-fractional signed number with a range of –9223372036854775808 to 9223372036854775807. Normalized to a series of decimal digits with no seperators. It is prefixed with minus (-) if the number is negative. Otherwise, there is no prefix."

define_type float
    describe en
        title "Float (Decimal Number)"
        body "A real number in specified by IEEE 754. It is normalized to standard scientific notation as commonly found in computers. For example, 123.4 is represented as `1.234e+2`."

define_type hexadecimal
    describe en
        title "Hexadecimal Sequence"
        body "A series of hexadecimal digits. Each digit is either a numeric digit (0 to 9) or a latin character of either 'a', 'b', 'c', 'd', 'e', or 'f'. All other characters are ignored and removed."
'''
