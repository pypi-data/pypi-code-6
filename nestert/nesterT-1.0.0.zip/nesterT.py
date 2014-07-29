# -*- coding: cp1252 -*-
""" This is the nesterT.py" module, and it provides one function called 
    printLOL() which prints lists that may or may not include nested lists.
    This file is extracted on nester.py in the book Head First Python
"""
def printLOL(the_list):
    """ This function takes a positional argument called "the_list", which is any 
        Python list (of, possibly, nested lists). Each data item in the provided list 
        is (recursively) printed to the screen on its own line.
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            printLOL(each_item)
        else:
            print(each_item)
""" Testing code:
movies = [
"The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
["Graham Chapman",
["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

print_lol(movies)

"""
