from configman.config_exceptions import CannotConvertError
import __builtin__
from functools import partial


#------------------------------------------------------------------------------
def last_repeat_generator(iterable):
    for x in iterable:
        yield x
    while True:
        yield x

#------------------------------------------------------------------------------
def memoize_function (max_cache_size=1000, arg_type_index=0):
    """Python 2.4 compatible memoize decorator.
    It creates a cache that has a maximum size.  If the cache exceeds the max,
    it is thrown out and a new one made.  With such behavior, it is wise to set
    the cache just a little larger that the maximum expected need.

    Parameters:
      max_cache_size - the size to which a cache can grow

    Limitations:
      The cache works only on args, not kwargs
    """
    def wrapper (f):
        def fn (*args):
            # Python says True == 1, therefore if we cache based on value alone
            # for the cases of True and 1, then we have ambiguity.  This is a
            # hack to differentiate them based on type for the cache.
            key = (args, type(args[arg_type_index]))
            try:
                result = fn.cache[key]
                return fn.cache[key]
            except KeyError:
                if fn.count >= max_cache_size:
                    fn.cache = {}
                    fn.count = 0
                result = f(*args)
                fn.cache[key] = result
                fn.count += 1
                return result
            except TypeError:
                return f(*args)
        fn.cache = {}
        fn.count = 0
        return fn
    return wrapper
memoize_instance_method = partial(memoize_function, arg_type_index=1)

#------------------------------------------------------------------------------
# a bunch of known mappings of builtin items to strings
known_mapping_type_to_str = dict(
    (val, key) for key, val in __builtin__.__dict__.iteritems()
    if val not in (True, False)
)

#------------------------------------------------------------------------------
@memoize_function(1000)
def _arbitrary_object_to_string(a_thing):
    """take a python object of some sort, and convert it into a human readable
    string"""
    # is it None?
    if a_thing is None:
        return ''
    # is it already a string?
    if isinstance(a_thing, basestring):
        return a_thing
    # does it have a to_str function?
    try:
        return a_thing.to_str()
    except (AttributeError, KeyError, TypeError), x:
        # nope, no to_str function
        pass
    # is it a built in?
    try:
        return known_mapping_type_to_str[a_thing]
    except (KeyError, TypeError):
        # nope, not a builtin
        pass
    # is it something from a loaded module?
    try:
        if a_thing.__module__ not in ('__builtin__', 'exceptions'):
            return "%s.%s" % (a_thing.__module__, a_thing.__name__)
    except AttributeError:
        # nope, not one of these
        pass
    # maybe it has a __name__ attribute?
    try:
        return a_thing.__name__
    except AttributeError:
        # nope, not one of these
        pass
    # punt and see what happens if we just cast it to string
    return str(a_thing)


#==============================================================================
class AnyInstanceOf(object):
    def __init__(self, a_type):
        self.a_type = a_type


#==============================================================================
class ConverterElement(object):
    def __init__(
        self,
        conversion_subject,
        converter_function,
        conversion_objective=str
    ):
        self.convertion_subject = conversion_subject
        self.converter_function = converter_function
        self.conversion_objective = conversion_objective
        self.subject_key = _arbitrary_object_to_string(conversion_subject)
        self.converter_function_key = _arbitrary_object_to_string(
            conversion_subject
        )
        self.objective_key = _arbitrary_object_to_string(conversion_objective)

    #--------------------------------------------------------------------------
    @memoize_instance_method(1000)
    def __call__(self, a_value):
        try:
            value_as_string = self.converter_function(a_value)
            if self.conversion_objective is str:
                return value_as_string
            else:
                final = self.conversion_objective(value_as_string)
                return final
        except (TypeError, ValueError), x:
            CannotConvertError(
                'Converting %s to %s failed: %s' %
                (self.subject_key, self.objective_key, x)
            )


#==============================================================================
class ConverterService(object):
    #--------------------------------------------------------------------------
    def __init__(self):
        self.library_by_subject_objective = {}  # keyed by tuple(
                                                # subject_key,
                                                # objective_key)
        # does this one need the 'subject' too?
        self.library_by_function_objective = {}  # keyed by tuple(
                                                 #converter_function_key,
                                                 # objective_key)
        self.library_by_instance_of_objective = {}  # keyed by tuple(
                                                    # subject_key,
                                                    # objective_key
        self.no_match_library = {}  # keyed by objective_key for use when all
                                    # else fails

    #--------------------------------------------------------------------------
    def register_converter(
        self,
        conversion_subject,
        converter_function,
        conversion_objective=str,
        force = False  # overwrite is ok
    ):
        if isinstance(conversion_subject, AnyInstanceOf):
            a_converter_element = ConverterElement(
                conversion_subject.a_type,
                converter_function,
                conversion_objective
            )
            key = (
                a_converter_element.subject_key,
                a_converter_element.objective_key,
            )
            if key not in self.library_by_instance_of_objective or force:
                self.library_by_instance_of_objective[key] = \
                    a_converter_element
        else:
            a_converter_element = ConverterElement(
                conversion_subject,
                converter_function,
                conversion_objective
            )
            key = (
                a_converter_element.subject_key,
                a_converter_element.objective_key,
            )
            if key not in self.library_by_subject_objective or force:
                self.library_by_subject_objective[key] = a_converter_element
                self.library_by_function_objective[(
                    a_converter_element.converter_function_key,
                    a_converter_element.objective_key,
                )] = a_converter_element


    #--------------------------------------------------------------------------
    def register_no_match_converter(self, a_type_key, a_conversion_function):
        self.no_match_library[a_type_key] = a_conversion_function

    #--------------------------------------------------------------------------
    @staticmethod
    def lookup_without_keyerror(mapping, key):
        try:
            return mapping[key]
        except KeyError:
            return None

    #--------------------------------------------------------------------------
    def converter_search_generator(
        self,
        a_thing,
        objective_key,
        converter_function_key,
    ):
        if converter_function_key is None:
            a_thing_type_key = _arbitrary_object_to_string(type(a_thing))
            yield self.lookup_without_keyerror(
                self.library_by_instance_of_objective,
                (a_thing_type_key, objective_key)
            )
            a_thing_key = _arbitrary_object_to_string(a_thing)
            yield self.lookup_without_keyerror(
                self.library_by_subject_objective,
                (a_thing_key, objective_key)
            )
            yield self.lookup_without_keyerror(
                self.no_match_library,
                objective_key
            )
        else:
            # here's where we get the abilty to find and existing converter
            # and override it with a new something different.  Local for_*
            # handlers may require their own converters for local types.  An
            # option may have a converter assigned that needs to be overridden
            yield self.lookup_without_keyerror(
                self.library_by_function_objective,
                (converter_function_key, objective_key),
            )


    #--------------------------------------------------------------------------
    @memoize_instance_method(1000)
    def convert(
        self,
        a_thing,
        objective_key='str',
        converter_function_key=None,  # used to lookup a
    ):
        for converter_element in self.converter_search_generator(
            a_thing, converter_function_key, objective_key
        ):
            try:
                converted_thing = converter_element(a_thing)
                return converted_thing
            except TypeError:
                # likely "None not callable"
                pass
            except Exception, x:
                raise CannotConvertError(
                    "There is no converter for '%s' to '%s'" % (
                        _arbitrary_object_to_string(a_thing),
                        objective_key
                    )
                )

#==============================================================================
#class ConverterLibrary(object):
    #def __init__(self)

converter_service = ConverterService()
#------------------------------------------------------------------------------
def to_str(a_thing):
    return converter_service.convert(a_thing, 'str')

#------------------------------------------------------------------------------
# register built in converters
#------------------------------------------------------------------------------
def make_identity_converter(key):
    def identitiy_converter(x):
        return key
    return identitiy_converter

#------------------------------------------------------------------------------
for key, value in __builtin__.__dict__.iteritems():
    converter_service.register_converter(
        value,
        make_identity_converter(key),
        str
    )

#------------------------------------------------------------------------------
import types
for key, value in types.__dict__.iteritems():
    converter_service.register_converter(
        value,
        make_identity_converter(key),
        str
    )

#------------------------------------------------------------------------------
# add known converters
converter_service.register_converter(bool, str, str)
converter_service.register_converter(True, str, str)
converter_service.register_converter(False, str, str)

#------------------------------------------------------------------------------
converter_service.register_no_match_converter(
    'str',
    _arbitrary_object_to_string
)
#------------------------------------------------------------------------------
# specialty converters
#------------------------------------------------------------------------------
def sequence_to_string(a_list, delimiter=", "):
    """a dedicated function that turns a list into a comma delimited string
    of items converted.  This method will flatten nested lists."""
    return delimiter.join(to_str(x) for x in a_list)

converter_service.register_converter(
    AnyInstanceOf(list),
    sequence_to_string,
    conversion_objective=str
)

def stupid_int_converter(an_int):
    return str(an_int * 10)

#converter_service.register_converter(
    #AnyInstanceOf(int),
    #stupid_int_converter,
    #conversion_objective=str
#)

def my_bool(a_bool):
    if a_bool:
        return 'ja ja ja'
    return 'nein nein nein'

converter_service.register_converter(AnyInstanceOf(bool), my_bool, force=True)

print converter_service.convert([1,3,5,7,11])



converter_service.convert(True)

