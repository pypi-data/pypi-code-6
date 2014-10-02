# rolne/xml.py
#
# xml support for rolne
#
#

# from . import rolne

def start_name(r, name):
    r.append(name, None)
    return r[name, None, -1]

def add_to_parent(r, name, value):
    r.append(name, value)
    return None

def finish_element(r, value, seq):
    if value:
        r.value = value
    parent = r.seq_parent(seq)
    if parent:
        return r.at_seq(parent)
    return r
    
def append_value(r, value):
    if value:
        if r.value:
            r.value = r.value+" "+value
        else:
            r.value = value
    return None
    
def parse_xml(text):
    # states possible
    ROOT = 0
    ELEMENT_NAME = 10
    WANDER = 20
    ATTR_SPACE = 30
    ATTR_NAME = 40
    ATTR_VALUE_BEFORE_QUOTE = 50
    ATTR_VALUE_DURING_QUOTE = 51
    CLOSE_ELEMENT = 60
    CONTENT = 70
    DONE = 1000
    #
    result = rolne()
    ptr = result
    state = ROOT
    next_name = ""
    ctr = 100
    for ch in text:
        if state==ROOT:
            if ch in ["<"]:
                state=ELEMENT_NAME
                next_name = ""
            else:
                continue
        elif state==ELEMENT_NAME:
            if ch in [" "]:
                state = ATTR_SPACE
                ptr = start_name(ptr, next_name)
                next_name = ""
            elif ch in ["/"]:
                state = CLOSE_ELEMENT
            elif ch in [">"]:
                state = WANDER
                ptr = start_name(ptr, next_name)
                next_name = ""
            else:
                next_name += ch
        elif state==ATTR_SPACE:
            if ch in [" "]:
                pass
            elif ch in [">"]:
                state = WANDER
            else:
                state = ATTR_NAME
                next_name = ch
        elif state==ATTR_NAME:
            if ch in [" "]:
                state = ATTR_SPACE
                next_name = ""
            elif ch in [">"]:
                state = WANDER
                next_name = ""
            elif ch in ["="]:
                state = ATTR_VALUE_BEFORE_QUOTE
                next_value = ""
            else:
                next_name += ch
        elif state==ATTR_VALUE_BEFORE_QUOTE:
            if ch in ['"']:
                state = ATTR_VALUE_DURING_QUOTE
            elif ch in [" "]:
                pass
            else:
                state = ATTR_SPACE
                next_name = ""
        elif state==ATTR_VALUE_DURING_QUOTE:
            if ch in ['"']:
                state=ATTR_SPACE
                add_to_parent(ptr, next_name, next_value)
                next_value = ""
                next_name = ""
            else:
                next_value += ch
        elif state==WANDER:
            if ch in ["<"]:
                state=ELEMENT_NAME
                next_name = ""
            elif ch in [" ", "\n"]:
                pass
            else:
                state = CONTENT
                next_value = ch
        elif state==CONTENT:
            if ch in ["<"]:
                state=ELEMENT_NAME
                append_value(ptr, next_value)
                next_name = ""
                next_value = ""
            else:
                next_value += ch
        elif state==CLOSE_ELEMENT:
            if ch in [">"]:
                state = WANDER
                ptr = finish_element(result, next_value, ptr.seq)
            else:
                pass
        elif state==DONE:
            print ch,
            continue
    return result

# eof