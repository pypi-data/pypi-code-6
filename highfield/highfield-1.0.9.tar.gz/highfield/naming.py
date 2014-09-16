import re

# Explicitly compile all regular expressions
# They will be cached anyway internally by python
# But this way we don't get the initial cache miss
case_change_regex = re.compile('[A-Z][^A-Z]*')
nonword_chars_regex = re.compile('[^\w\s]')
multiple_spaces_regex = re.compile('\s+')

def canonical_to_words(canonical):
    return ' '.join(p for p in canonical.split('_'))

def file_to_class(filename):
    return ''.join([ucfirst(p) for p in filename.split('_')])

def class_to_file(classname):
    return '_'.join([p.lower() for p in case_change_regex.findall(classname)])

def ucfirst(string, ignore_rest=False):
    return string[0].upper() + (string[1:] if ignore_rest else string[1:].lower())

def file_to_canonical(filename):
    return filename[:filename.rfind('_')]

def class_to_canonical(classname):
    return file_to_canonical(class_to_file(classname))

def string_to_classvar(string):
    return string_to_underscored_words(string).upper()

def string_to_methodname(string):
    return string_to_underscored_words(string).lower()

def string_to_words(string):
    return nonword_chars_regex.sub('', string)

def string_to_underscored(string):
    return multiple_spaces_regex.sub('_', string)

def string_to_underscored_words(string):
    return string_to_underscored(string_to_words(string))

def string_to_slug(string):
    return multiple_spaces_regex.sub('-', string_to_words(string)).lower()

def content_subtype(content_type):
    return content_type[content_type.find('/') + 1:].upper()

def singular(string):
    return string[:-1]

def enumeration(sequence):
    if not len(sequence):
        return ''
    if len(sequence) is 1:
        return sequence[0]
    return '%s and %s' % (', '.join(sequence[:-1]), sequence[-1])
