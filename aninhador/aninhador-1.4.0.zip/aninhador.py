"""This is the "aninhador.py" module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists"""
import sys
def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """This function takes a positional argument called "the_list", which is
    any Python list (of, possibly, nested lists). Each data item in the
    provided list is (recursively) printed to the screen on its own line.
    A second argument called "indent" determines if the list in printed with
    identation on each of its nested lists. A third argument called "level"
    is used to insert tab-stops when a nested list is encountered. A fourth
    argument called "filename" indicades output file for the list. If no file
    is indicated, the list is printed on standard output"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                print('\t' * level, end='', file=fh)
            print(each_item, file=fh)
