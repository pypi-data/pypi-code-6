#!/usr/bin/python
import json, sys, argparse

def manipulate(json_object, key, rest):
    """ 
    Manipulate a dictionary.

    Args:
        json_object: dictionary or list to manipulate
        key:
            1) string            -> select only given key from dictionary
            2) list of strings   -> select only given keys from dictionary
                                    or select only given keys from the dictionaries
                                    in the given list
            3) None              -> return given dictionary or list untouched
        rest:
            1) tuple (key, rest) -> recursively call manipulate on the by key selected
                                    part of the dictionary or list
            2) None              -> end recursive calls
    Returns:
        Manipulated dictonary or list
    """
    
    # json_object is list: select key from list of dictionaries
    if type(json_object) == list:
        return [manipulate(item, key, rest) for item in json_object]
    
    # key is string: select key from dictionary
    if type(key) == str:
        if key in json_object:
            if not rest is None:
                rest_object = manipulate(json_object[key], rest[0], rest[1])
            else:
                rest_object = json_object[key]
            return {key : rest_object}
        else:
            raise KeyNotFound(key)
    
    # key is list: select keys from dictionary
    if type(key) == list:
        return_object = {}
        for sub_key in key:
            return_object[sub_key[0]] = manipulate(json_object, sub_key[0], sub_key[1])[sub_key[0]]
        return return_object
        
    if key == None:
       return json_object
   
def get_key(ms):
    """
    Creates a key and a rest tuple based on a manipulation string
    
    Args:
        ms: Manipulation string
            eg. '', 'result','result.rows' or 'result.rows[name|address]'
    Returns:
        A tuple of key and rest. In the above example respectivly:
            (None, None)
            ('result', None)
            ('result', ('rows', None))
            ('result', ('rows', (['name', 'address'], None)))
    """
    if ms == '':
        return (None, None)
    
    if type(ms) == str:
        dot_pos = ms.find('.')
        pipe_pos = ms.find('|')
        parenthesis_pos = ms.find('(')
        square_bracket_pos = ms.find('[')
        square_bracket_end_pos = ms.find(']')
    
        # remove starting and trailing parenthesis
        if parenthesis_pos == 0:
            ms = remove_starting_and_trailing_character(ms, ('(',')'))
            parenthesis_pos = -1
            
        # remove starting and trailing square_brackets
        if square_bracket_pos == 0:
            ms = remove_starting_and_trailing_character(ms, ('[',']'))
            square_bracket_pos = -1
        
        # check positions of brackets, parethesis and pipes
        no_dot_before_brackets = (dot_pos == -1 or dot_pos > square_bracket_pos)
        pipe_not_inside_parenthesis = (parenthesis_pos == -1 or pipe_pos < parenthesis_pos)
        pipe_not_inside_brackets = (square_bracket_pos == -1 or pipe_pos < square_bracket_pos or pipe_pos > square_bracket_end_pos)
        pipe_inside_brackets = square_bracket_pos != -1 and (not pipe_pos > square_bracket_end_pos or square_bracket_end_pos == -1)
        
        # return (key, rest) tuple
        if no_dot_before_brackets and pipe_inside_brackets:
            rest_string = remove_starting_and_trailing_character(ms[square_bracket_pos:], ('[',']'))
            return (ms[:square_bracket_pos], get_key(rest_string))
        
        # return list of (key, rest) tuples
        if pipe_pos != -1 and pipe_not_inside_parenthesis and pipe_not_inside_brackets:
            return (map(get_key, get_piped_parts(ms)), None)
        
        # return (key, rest) tuple
        if dot_pos != -1:
            return (ms[:dot_pos], get_key(ms[dot_pos+1:]))
        
        return (ms, None)

def remove_starting_and_trailing_character(value, character_couple):
    
    if value[-1] != character_couple[1] and value[0] != character_couple[0]:
        return value
    elif value[-1] != character_couple[1]:
        raise ParseError("missing trailing '" + character_couple[1] + "'")
    elif value[0] != character_couple[0]:
        raise ParseError("missing opening '" + character_couple[0] + "'")
    else:
        return value[1:-1]

def get_piped_parts(ms):
    """
    Splits a string on the pipe '|' character, but only if it
    is not inside parenthesis () or square brackets [].
    
    Args:
        ms: Manipulation string
    Returns:
        List of strings
    """
    if ms == '':
        return []
        
    pipe_pos = ms.find('|')
    square_bracket_pos = ms.find('[')
    square_bracket_end_pos = ms.find(']')
    parenthesis_pos = ms.find('(')
    
    pipe_inside_brackets = (square_bracket_pos != -1 and pipe_pos > square_bracket_pos and pipe_pos < square_bracket_end_pos)
    
    if pipe_pos == -1 or (parenthesis_pos != -1 and pipe_pos > parenthesis_pos) or (pipe_inside_brackets):
        return [ms]
    
    return [ms[:pipe_pos]] + get_piped_parts(ms[pipe_pos+1:])

def get_args(argument_list):
    """
    Returns an object with command line arguments.
    """
    parser = argparse.ArgumentParser(description='Show and manipulate json strings.')
    parser.add_argument('-m', '--manipulate_string', type=str, default='', help='A maniputation string, see description.')
    return parser.parse_args(argument_list[1:])

class KeyNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def main():
    # load the json_object from the stdin
    try:
        json_object = json.load(sys.stdin)
    except ValueError:
        print "Error: malformed JSON-string!"
        exit(2)

    # parse command line arguments
    args = get_args(sys.argv)
    
    # create json manipulation object based on command line arguments
    try:
        (key, rest) = get_key(args.manipulate_string)
    except ParseError as e:
        print "Parse error: " + e.value + "!"
        exit(3)
        
    # create the manipulated json object
    try:
        json_object = manipulate(json_object, key, rest)
    except KeyNotFound as e:
        print "Error: '" + e.value + "' was not found!"
        exit(1)
    
    # print the manipulated json object to screen
    print json.dumps(json_object, indent=4, separators=(',', ': '))
