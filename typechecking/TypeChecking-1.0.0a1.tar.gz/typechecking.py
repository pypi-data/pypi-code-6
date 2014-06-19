import collections
from collections import abc as cabc
import functools
import inspect
import itertools
import logging
import sys
import types
import warnings

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class InvalidTypeHintError(Exception):
    """Exception indicating an invalid type hint.

    Raised when a decorated function uses an invalid type hint as an
    annotation, either of a parameter or of the return type.

    """
    pass

def _find_ellipsis(t: tuple) -> int:
    for idx, value in enumerate(t):
        if value is Ellipsis:
            return idx
    else:
        return None

@functools.singledispatch
def _match_foo(annotation: object, value: object, strict: bool) -> bool:
    assert False

@_match_foo.register(type)
def _match_type(annotation: type, value: object, strict: bool) -> bool:
    logger.debug('Matching %r against type %r', value, annotation)
    result = isinstance(value, annotation)
    if not result:
        logger.info('%r is not an instance of %r', value, annotation)
    return result

@_match_foo.register(tuple)
def _match_tuple(annotation: tuple, value: object, strict: bool) -> bool:
    logger.debug('Matching %r against tuple-hint %r', value, annotation)
    if not isinstance(value, tuple):
        logger.info('%r is not a tuple', value)
        return False
    ellipsis_idx = _find_ellipsis(annotation)
    if ellipsis_idx is not None:
        assert ellipsis_idx != 0
        hint_before = tuple(annotation[:ellipsis_idx-1])
        hint_at = annotation[ellipsis_idx-1]
        hint_after = tuple(annotation[ellipsis_idx+1:])

        assert _find_ellipsis(hint_after) is None
        logger.debug('Split type hint into %r, %r, and %r', hint_before,
                     hint_at, hint_after)

        value_before = tuple(value[:len(hint_before)])
        if hint_after:
            value_at = value[len(hint_before):-len(hint_after)]
            value_after = tuple(value[-len(hint_after):])
        else:
            value_at = value[len(hint_before):]
            value_after = ()
        logger.debug('Split argument into %r, %r, and %r', value_before,
                     value_at, value_after)
        result = (_match_tuple(hint_before, value_before, strict) and
                  _match_tuple(hint_after, value_after, strict))
        return result and all(_match(hint_at, x, strict) for x in value_at)
    else:
        if len(annotation) != len(value):
            logger.info('%r is wrong length, compare to %r', value,
                        annotation)
            return False
        return all(_match(x, y, strict) for x, y in zip(annotation, value))

@_match_foo.register(list)
def _match_list(annotation: list, value: object, strict: bool) -> bool:
    assert len(annotation) == 1
    logger.debug('Matching %r against sequence-hint %r', value, annotation)
    if strict and not isinstance(value, list):
        logger.info("%r is not a list and we're in strict mode", value)
        return False
    if not isinstance(value, cabc.Iterable):
        logger.info('%r is not iterable', value)
        return False
    if not isinstance(value, cabc.Sequence):
        logger.debug('Only check the contents of sequences, not %r', value)
        return True
    return all(_match(annotation[0], x, strict) for x in value)

@_match_foo.register(dict)
def _match_dict(annotation: dict, value: object, strict: bool) -> bool:
    assert len(annotation) == 1
    logger.debug('Matching %r against mapping-hint %r', value, annotation)
    if strict and not isinstance(value, dict):
        logger.info("%r is not a dict and we're in strict mode", value)
        return False
    if not isinstance(value, cabc.Mapping):
        logger.info('%r is not a mapping', value)
        return False
    ((ktype, vtype),) = annotation.items()
    result = all(_match(ktype, k, strict) for k in value.keys())
    return result and all(_match(vtype, v, strict) for v in value.values())

@_match_foo.register(str)
def _match_str(annotation: str, value: object, strict: bool) -> bool:
    logger.debug('Matching %r against string-hint %r', value, annotation)
    try:
        modname, typename = annotation.rsplit('.', 1)
    except ValueError:
        annotation = 'builtins.' + annotation
        logger.debug('Expanded hint to %r', annotation)
        modname, typename = annotation.rsplit('.', 1)
    try:
        module = sys.modules[modname]
    except KeyError:
        logger.info('Module %r not yet imported, type mismatch assumed',
                     modname)
        return False
    try:
        klass = getattr(module, typename)
    except AttributeError:
        return False
    return _match(klass, value, strict)

@_match_foo.register(types.FunctionType)
def _match_func(annotation: types.FunctionType, value:object,
                strict: bool) -> bool:
    logger.debug('Matching %r against function-hint %r', value, annotation)
    return annotation(value)

@_match_foo.register(type(None))
def _match_none(annotation: type(None), value: object, strict: bool) -> bool:
    logger.debug('Matching %r against None', value)
    return value is None

def _match(annotation: object, value: object, strict: bool) -> bool:
    if (not strict) and value is None:
        return True
    if not _valid_hint(annotation):
        raise InvalidTypeHintError(annotation)
    try:
        return _match_foo(annotation, value, strict)
    except TypeError:
        logger.info('TypeError raised, assuming mismatch', exc_info=True)
        return False
    except AssertionError:
        raise
    except Exception:
        logger.exception('Unexpected exception raised, assuming match')
        return True

@functools.singledispatch
def _valid_hint(annotation: object) -> bool:
    return False

@_valid_hint.register(type(None))
@_valid_hint.register(type)
@_valid_hint.register(types.FunctionType)
def _valid_trivial(annotation: object) -> bool:
    return True

@_valid_hint.register(list)
def _valid_seq(annotation: list) -> bool:
    return len(annotation) == 1 and _valid_hint(annotation[0])

@_valid_hint.register(dict)
def _valid_map(annotation: dict) -> bool:
    if not len(annotation) == 1:
        return False
    ((ktype, vtype),) = annotation.items()
    return _valid_hint(ktype) and _valid_hint(vtype)

@_valid_hint.register(str)
def _valid_str(annotation: str) -> bool:
    return ((not annotation.startswith('.')) and
            (not annotation.endswith('.')))

@_valid_hint.register(tuple)
def _valid_tuple(annotation: tuple) -> bool:
    idx = _find_ellipsis(annotation)
    if idx is None:
        return all(_valid_hint(x) for x in annotation)
    elif idx == 0:
        return False
    else:
        idx2 = _find_ellipsis(annotation[idx+1:])
        if idx2 is not None:
            return False
        return (all(_valid_hint(x) for x in annotation[:idx]) and
                all(_valid_hint(x) for x in annotation[idx+1:]))


def check(func: types.FunctionType, strict: bool=False) -> types.FunctionType:
    """Apply type checking to the given function.

    Wraps the function in a type checker.  When the wrapped function is
    called, if the arguments or the return value do not match their
    annotations, the checker raises TypeError.

    If strict is True, type checking is slightly more pedantic about certain
    distinctions, in particular requiring lists and dictionaries instead of
    sequences and mappings.

    Type checking is skipped entirely if Python was started with the -O flag.
    Reasonable code should be type-correct in the first place.  If client code
    decides to call a function incorrectly, it is ultimately the client's
    problem.

    Not all functions require type checking.  Type checking is provided as a
    decorator so that it may be applied selectively.  Functions which are
    called frequently or whose arguments are routinely very large may not be
    good candidates for regular type checking.

    """
    if not __debug__:
        return func
    sig = inspect.signature(func)
    params = sig.parameters
    for p in params.values():
        if not _valid_hint(p.annotation):
            raise InvalidTypeHintError(p.annotation)
    rtype = sig.return_annotation
    if not _valid_hint(rtype):
        raise InvalidHintError(rtype)
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for argname, value in bound.arguments.items():
            annotation = params[argname].annotation
            if not _match(annotation, value, strict):
                raise TypeError('Argument {!r} does not match type hint {!r}'
                                .format(value, annotation))
        result = func(*args, **kwargs)
        if not _match(rtype, result, strict):
            raise TypeError('Return value {!r} does not match type hint {!r}'
                            .format(result, rtype))
        return result
    return new_func

def check_strict(func: types.FunctionType) -> types.FunctionType:
    """Convenience function for strict type checking.

    Equivalent to functools.partial(check, strict=True).

    """
    return check(func, strict=True)

def check_class(klass: type) -> type:
    """Apply typechecking annotations to the given class.

    Attaches annotations to the self parameters of the methods in this
    class, which would otherwise be mildly annoying to annotate by hand.

    The methods are not automatically decorated with @check or @check_strict.

    """
    for name, value in klass.__dict__:
        if callable(value):
            sig = inspect.signature(value)
            params = sig.parameters
            self_name = next(iter(params))
            value.__annotations__[self_name] = klass
    return klass
