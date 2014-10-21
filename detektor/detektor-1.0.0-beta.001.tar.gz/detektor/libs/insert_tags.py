#!/bin/sh

import re
import sys
from time import sleep
from cStringIO import StringIO


def error(s):
    print s
    sleep(0.3)


def add_enddef(language, filehandler):
    #filesuffix = file[-2:]
    if language == 'python':
        return add_enddef_python(filehandler)
    elif language == 'perl':
        return add_enddef_perl(filehandler)


def add_enddef_perl(filehandler):
    fout = StringIO()
    line = filehandler.readline()
    while line:
        match = re.search(r"(^|\s+)sub\s+\w+", line)
        if match:
            # a function is found, and it's time to start looking for 
            num_blocks = 1
            first_found = 0
            while line:
                char_number = 0 # for knowing where to insert the 'enddef' tag
                for char in line:
                    char_number += 1
                    if char == '{':
                        if first_found:
                            num_blocks += 1
                        else:
                            first_found = 1
                    if char == '}':
                        num_blocks -= 1
                if num_blocks == 0:
                    line = line[:char_number] + "enddef " + line[char_number:]
                    break
                fout.write(line)
                line = filehandler.readline()
        fout.write(line)
        line = filehandler.readline()
    filehandler.close()
    fout.seek(0)
    return fout
        
        
def add_enddef_python(filehandler):
    # I'm pretty shure this could have been done a lot easier.
    # f = open(file, 'r')
    lines = filehandler.readlines()
    filehandler.close()

    # Has to use two patters to find functions since the regexp
    # r"(\s*)def\s\w+) with match.group(0) won't return only the
    # indent, but the whole line. Seams that picking out whites
    # is a special case.

    # If def occurs first in line, ptrn1 will match
    ptrn1 = r"^def\s[_|\w]+.+"
    # Else ptrn2 will
    ptrn2 = r"(\s+)def\s_*\w+"
    # This pattern matches global definitions
    indents1 = r"^[_|\w]+"
    # this matches funtions defined inside another structure
    indents2 = r"^(\s+[_|\w])"

    # tmp-counter
    empty_lines = 0
    
    for i in range(0, len(lines)+1, 1):
        if i >= len(lines):
            break
        match1 = re.search(ptrn1, lines[i])
        match3 = re.search(ptrn2, lines[i])
        if match1: # a global function is found 
            i += 1
            # run a separat for-loop inside function:
            for j in range(i, len(lines)+1, 1):
                # if the line is empty og comment, increase empty_lines
                match_empty = re.search(r"^\s*$", lines[j])
                match_comment = re.search(r"#.*", lines[j])
                if match_empty or match_comment:
                    empty_lines += 1
                # if match2 then the indents has ended
                match2 = re.search(indents1, lines[j])
                if match2:
                    lines.insert(j-empty_lines, "enddef\n")
                    break
                if not match_empty and not match_comment:
                    # reset empty_lines if more code is found
                    empty_lines = 0
                i += 1
    
        elif match3: # a indented def is found
            i += 1
            tab = match3.group(0)[:(match3.group(0).find("def"))]
            for j in range(i, len(lines)+1, 1):
                # count empty lines
                if j >= len(lines):
                    break
                if re.search(r"^\s*$", lines[j]) or re.search(r"#.*", lines[j]):
                    empty_lines += 1 
                
                match4 = re.search(indents2, lines[j])
                if match4:
                    # This is the only way I could determine the size of
                    # the tab found (a unecessary hack?) :
                    tab_len = len(match4.group(0)) - 1
                    if tab_len <= len(tab): # then an indent is found
                        lines.insert(j-empty_lines, (tab+"enddef\n"))
                        break
                    else:
                        empty_lines = 0
                i += 1
            
    return StringIO('\n'.join(lines))
                              
if __name__ == '__main__':
    try:
        add_enddef(sys.argv[1])
    except:
        print 'Could not find', sys.argv[1]
