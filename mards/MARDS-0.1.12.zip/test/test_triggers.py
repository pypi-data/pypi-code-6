import sys, os
# the action below is a no-no in standard python, but it is done here for
# easy on-the-fly testing.

# this setup assumes that MARDS is NOT in the python library on the local
# machine, but is instead in a parrallel directory.
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..'))
#print sys.path
import MARDS

doc = '''
#!MARDS_en_1.0

blink zippy
item "broom"
    size 33
    color blue
    blueness    
item "brush"
    size 2
'''

schema = '''
#!MARDS_schema_en_1.0 blah

name blink
    value
        type label
        required
    name rate
name item
    treatment unique
    value
        type label
        required
    name size
        treatment one
    name color
        treatment unique
    name title
        required
        treatment concat
        value
            default "unknown"
    search color
        match 'blue'
            search size
                match 33
                    name blueness
                        value
                            required
        match 'yellow'
            name yellowness

'''

# x,e = MARDS._SCHEMA_to_rolne(schema)
x,e = MARDS.string_to_rolne(doc, schema)
print "FINAL:\n"
print x._explicit()
print "ERRORS:\n"
print repr(e)
