#!/bin/sh
""":"
exec python $0 ${1+"$@"}
"""#"
import sys

def defgetter(language, s):
    if language == 'python':
        return defgetter_python(s)
    elif language == 'perl':
        return defgetter_perl(s)
    else:
        return None


def defgetter_perl(s):
    def_list = []
    while 1:
        n = s.find("sub")
        if n < 0:
            break
        s = s[n:]
        n = s.find("enddef")
        a_function = s[:n]
        def_list.append(a_function)
        s = s[n+6:]
    return def_list


def defgetter_python(s):
    def_list = []

    while 1:
        # remove everything before an occurence of 'def'
        n = s.find("def")
        if n < 0:
            # if no 'def' found; stop
            break
        s = s[n:]
        # find the end of the function (the inserted 'enddef')
        n = s.find("enddef")
        a_function = s[:n]
        def_list.append(a_function)
        s = s[n+6:]
        
    return def_list
