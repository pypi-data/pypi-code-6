"""High level abstraction of the detektor common functions.



"""
from detektor.libs.codeparser import Parser
from detektor.libs.comparer import Comparer
from detektor.libs.detektor_signature import DetektorSignature


def get_deep_attr(obj, attrs):
    for attr in attrs.split("."):
        obj = getattr(obj, attr)
    return obj


def has_deep_attr(obj, attrs):
    try:
        get_deep_attr(obj, attrs)
        return True
    except AttributeError:
        return False


def compare(objects):
    percentage = 20
    c = Comparer(objects, percentage)
    return c.get_result()


def set_detektor_signature(language, obj, filepath_attribute):
    """Set the "detektor_signature" on list of, or object.

    Arguments:
    language -- The programming language in the file.
    obj -- The obj that the detektor_signature attribute should be added to. Assumed to be iterable.
    filepath_attribute -- The attribute that holds the attribute path.

    Examples:
    set_detektor_signature_on_single_object(assignment, 'fileobj.path')
    """
    try:
        return set_detektor_signature_on_list_of_objects(language, obj, filepath_attribute)
    except:
        return set_detektor_signature_on_single_object(language, obj, filepath_attribute)


def get_detektor_signature_from_file(language, filepath):
    """Reads a file and returns a detektor signature as dict. """
    filehandler = open(filepath, 'r')
    p = Parser(language, filehandler)
    return p.get_code_signature()


def set_detektor_signature_on_single_object(language, obj, filepath_attribute):
    """Set the "detektor_signature" on the object.

    Arguments:
    language -- The programming language in file.
    obj -- The obj that the detektor_signature attribute should be added to.
    filepath_attribute -- The attribute that holds the file path of the code.

    Examples:
    set_detektor_signature_on_single_object(assignment, 'fileobj.path')
    """
    if not has_deep_attr(obj, filepath_attribute):
        raise AttributeError('{} does not exist for {}'.format(filepath_attribute, obj))
    filepath = get_deep_attr(obj, filepath_attribute)
    filehandler = open(filepath, 'r')
    p = Parser(language, filehandler)
    code_signature = p.get_code_signature()
    obj.detektor_signature = DetektorSignature(**code_signature)
    return obj


def set_detektor_signature_on_list_of_objects(language, object_list, filepath_attribute):
    """Set the "detektor_signature" on a list of objects.

    Arguments:
    object_list -- The list of objects that the detektor_signature attribute should be added to.
    filepath_attribute -- The attribute that holds the file path of the code.

    Examples:
    set_detektor_signature_on_list_of_objects(assignments, 'fileobj.path')
    """
    return [set_detektor_signature_on_single_object(language, o, filepath_attribute) for o in object_list]
