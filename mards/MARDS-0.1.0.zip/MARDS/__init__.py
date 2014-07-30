# MARDS\__init__.py
#
# MARDS data serialization library
#
# Version 0.1.0

from rolne import rolne

import mards_library as ml

def string_to_rolne(doc=None, tab_strict=False):
    result = rolne()
    current = 0
    tab_list = [0]
    pointer_list = range(50)
    pointer_list[0]=result
    for ctr, line in enumerate(doc.split("\n")):
        (indent, key, value, error) = ml.parse_line(line, tab_list, tab_strict=tab_strict)
        if error:
            print "error in document line {c}: {e}".format(e=error, c=ctr)
        else:
            if key:
                if indent<current:
                    current = indent
                elif indent==current:
                    pass # do nothing, the operational default works
                elif indent==(current+1):
                    pointer_list[indent] = last_spot
                    current = indent
                else:
                    print "tab error in document line {c}".format(c=ctr)
                    print indent, current
                pointer_list[indent].append(key, value)
                last_spot = pointer_list[indent][key, value, -1]
    return result


def rolne_to_string(r, tab_size=4, quote_all=True):
    result = ""
    #print r.data
    if r:
        for (rn, rv, rl) in r.data:
            result += rn
            if rv is not None:
                printable = str(rv)
                quote_flag = False
                if '"' in printable:
                    quote_flag = True
                if len(printable) != len(printable.strip()):
                    quote_flag = True
                if quote_flag or quote_all:
                    result += " "+'"'+rv+'"'
                else:
                    result += " "+rv
            result += "\n"
            if rl:
                temp = rolne_to_string(rolne(in_list=rl), tab_size=tab_size, quote_all=quote_all)
                for line in temp.split("\n"):
                    if line:
                        result += " "*tab_size+line
                        result += "\n"
    return result

if __name__ == "__main__":

    if True:

        my_doc = '''
item zing
    size 4
    color red
        intensity 44%
    color yellow
item womp
    size 5
    color blue
item bam
item bam
item broom
    size 7
    title "The "big" thing"
zoom_flag
code_seq
    * r9
    * r3
    * r2
    * r3
system_title hello'''

        #print my_doc
        r = string_to_rolne(my_doc)
        print rolne_to_string(r, quote_all=False)

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
