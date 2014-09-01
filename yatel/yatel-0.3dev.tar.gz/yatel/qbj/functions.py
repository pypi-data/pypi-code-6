#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# DOCS
#===============================================================================

"""QBJ domain of functions.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import inspect, collections
import datetime as dt

from yatel import stats
from yatel import db
from yatel.cluster import kmeans as _kmeans


#===============================================================================
# MAP
#===============================================================================

FUNCTIONS = collections.OrderedDict()

PRIVATE_FUNC_DATA = ["func"]


#==============================================================================
# CLASS
#==============================================================================

#: doc
QBJFunction = collections.namedtuple(
    "QBJFunction", ["name", "doc", "func"]
)


#===============================================================================
# REGISTER FUNCTION
#===============================================================================

def qbjfunction(name=None, doc=None):

    def _dec(func):
        qbjfunc = QBJFunction(
            name=name or func.__name__,
            doc=doc or func.__doc__,
            func=func
        )
        FUNCTIONS[qbjfunc.name] = qbjfunc
        if doc is not None:
            func.__doc__ = doc
        return func

    return _dec


def pformat_data(fname):
    fdata = FUNCTIONS[fname]
    data = {}
    for k, v in fdata._asdict().items():
        if k not in PRIVATE_FUNC_DATA:
            data[k] = v
    return data


def execute(name, nw, *args, **kwargs):
    return FUNCTIONS[name].func(nw, *args, **kwargs)


#==============================================================================
# HELP FUNCTION
#==============================================================================

@qbjfunction()
def ping(nw):
    """Always return True"""
    return True

@qbjfunction()
def help(nw, fname=None):
    """Returns a list of all functions if `fname` is not specified or ``None``
    otherwise documentation for `fname`.
    """
    if fname is None:
        return list(FUNCTIONS.keys())
    return pformat_data(fname)


#==============================================================================
# YATEL NETWORK
#==============================================================================

@qbjfunction(doc=db.YatelNetwork.haplotypes.__doc__)
def haplotypes(nw):
    return nw.haplotypes()


@qbjfunction(doc=db.YatelNetwork.haplotype_by_id.__doc__)
def haplotype_by_id(nw, hap_id):
    return nw.haplotype_by_id(hap_id)


@qbjfunction(doc=db.YatelNetwork.haplotypes_by_environment.__doc__)
def haplotypes_by_environment(nw, env=None, **kwargs):
    return nw.haplotypes_by_environment(env=env, **kwargs)


@qbjfunction(doc=db.YatelNetwork.edges.__doc__)
def edges(nw):
    return nw.edges()


@qbjfunction(doc=db.YatelNetwork.edges_by_haplotype.__doc__)
def edges_by_haplotype(nw, hap):
    return nw.edges_by_haplotype(hap)


@qbjfunction(doc=db.YatelNetwork.edges_by_environment.__doc__)
def edges_by_environment(nw, env=None, **kwargs):
    return nw.edges_by_environment(env=env, **kwargs)


@qbjfunction(doc=db.YatelNetwork.facts.__doc__)
def facts(nw):
    return nw.facts()


@qbjfunction(doc=db.YatelNetwork.facts_by_haplotype.__doc__)
def facts_by_haplotype(nw, hap):
    return nw.facts_by_haplotype(hap)


@qbjfunction(doc=db.YatelNetwork.facts_by_environment.__doc__)
def facts_by_environment(nw, env=None, **kwargs):
    return nw.facts_by_environment(env=env, **kwargs)


@qbjfunction(doc=db.YatelNetwork.describe.__doc__)
def describe(nw):
    return nw.describe()


@qbjfunction(doc=db.YatelNetwork.environments.__doc__)
def environments(nw, facts_attrs=None):
    return nw.environments(facts_attrs=facts_attrs)


#==============================================================================
# STATS
#==============================================================================

@qbjfunction(doc=stats.amax.__doc__)
def amax(nw, env=None, **kwargs):
    return stats.amax(nw, env=env, **kwargs)


@qbjfunction(doc=stats.amin.__doc__)
def amin(nw, env=None, **kwargs):
    return stats.amin (nw, env=env, **kwargs)


@qbjfunction(doc=stats.average.__doc__)
def average(nw, env=None, **kwargs):
    return stats.average(nw, env=env, **kwargs)


@qbjfunction(doc=stats.env2weightarray.__doc__)
def env2weightarray(nw, env=None, **kwargs):
    return stats.env2weightarray(nw, env=env, **kwargs)


@qbjfunction(doc=stats.kurtosis.__doc__)
def kurtosis(nw, env=None, **kwargs):
    return stats.kurtosis(nw, env=env, **kwargs)


@qbjfunction(doc=stats.max.__doc__)
def max(nw, env=None, **kwargs):
    return stats.max(nw, env=env, **kwargs)


@qbjfunction(doc=stats.median.__doc__)
def median(nw, env=None, **kwargs):
    return stats.median(nw, env=env, **kwargs)


@qbjfunction(doc=stats.min.__doc__)
def min(nw, env=None, **kwargs):
    return stats.min(nw, env=env, **kwargs)


@qbjfunction(doc=stats.mode.__doc__)
def mode(nw, env=None, **kwargs):
    return stats.mode(nw, env=env, **kwargs)


@qbjfunction(doc=stats.percentile.__doc__)
def percentile(nw, q, env=None, **kwargs):
    return stats.percentile(nw, q, env=env, **kwargs)


@qbjfunction(doc=stats.range.__doc__)
def range(nw, env=None, **kwargs):
    return stats.range(nw, env=env, **kwargs)


@qbjfunction(doc=stats.env2weightarray.__doc__)
def std(nw, env=None, **kwargs):
    return stats.std(nw, env=env, **kwargs)


@qbjfunction(doc=stats.sum.__doc__)
def sum(nw, env=None, **kwargs):
    return stats.sum(nw, env=env, **kwargs)


@qbjfunction(doc=stats.var.__doc__)
def var(nw, env=None, **kwargs):
    return stats.var(nw, env=env, **kwargs)


@qbjfunction(doc=stats.variation.__doc__)
def variation(nw, env=None, **kwargs):
    return stats.variation(nw, env=env, **kwargs)


#==============================================================================
# DM
#==============================================================================

@qbjfunction(doc=_kmeans.kmeans)
def kmeans(nw, envs, k_or_guess, whiten=False, coords=None, *args, **kwargs):
    """Performs k-means on a set of all environments defined by `fact_attrs`
    of a network.

    Parameters
    ----------
    nw : `yatel.db.YatelNetwork`
        Network source of environments to classify.
    envs : iterable of `yatel.dom.Environments` or dicts
        Represents all the environments to be clustered.
    k_or_guess : int or ndarray
        The number of centroids to generate. A code is assigned
        to each centroid, which is also the row index of the
        centroid in the code_book matrix generated.

        The initial k centroids are chosen by randomly
        selecting observations from the observation matrix.
        Alternatively, passing a k by N array specifies the
        initial k centroids.
    whiten : bool
        execute ``scipy.cluster.vq.whiten`` function over the
        observation array before executing subjacent *scipy kmeans*.
    coordc : None or callable
        If `coordc` is ``None`` generates use `hap_in_env_coords`
        function. Otherwise `coordc` must be a callable with
        2 arguments:

        - `nw` network source of environments to classify.
        - `env` the environment to calculate the coordinates

        and must return an array of coordinates for the given
        network environment.
    args : arguments for scipy kmeans
    kwargs : keywords arguments for scipy kmeans

    Returns
    -------
    coodebook : an array kxn of k centroids
        A k by N array of k centroids. The i’th
        centroid codebook[i] is represented with the
        code i.
        The centroids and codes generated represent
        the lowest distortion seen, not necessarily
        the globally minimal distortion.
    distortion : the value of the distortion
        The distortion between the observations
        passed and the centroids generated.

    """
    def dcoords(nw, env):
        return coords[env]

    coordc = dcoords if coords else None

    return _kmeans.kmeans(
        nw=nw, envs=envs, k_or_guess=k_or_guess,
        whiten=whiten, coordc=coordc, *args, **kwargs
    )


#===============================================================================
# GENERIC ITERATION
#===============================================================================

@qbjfunction()
def slice(nw, iterable, f, t=None):
    """Returns `iterable` from F-th element to T-th element.

    Parameters
    ----------
    nw : `yatel.db.YatelNetwork`
        network source of data.
    iterable : iterator
        iterable object.
    f : int
        Starting point.
    t : int or None
        Finishing point.

    """
    if t is None:
        return iterable[f:]
    return iterable[f:t]


@qbjfunction()
def size(nw, iterable):
    """Returns size of `iterable`.

    """
    return len(iterable)


@qbjfunction()
def sort(nw, iterable, key=None, dkey=None, reverse=False):
    """Sorts `iterable` using one of it's keys as reference.

    Parameters
    ----------
    nw : `yatel.db.YatelNetwork`
        network source of data.
    iterable : iterator
        iterable object.
    key : str or None
        A key of objects in `iterable` to sort.
    dkey : str or None
        Defalut key to sort.

    """

    def keyextractor(elem):
        if isinstance(elem, collections.Mapping):
            return elem.get(key, dkey)
        return getattr(elem, key, dkey)

    if key is None:
        return sorted(iterable, reverse=reverse)
    return sorted(iterable, key=keyextractor, reverse=reverse)


@qbjfunction()
def index(nw, iterable, value, start=None, end=None):
    """Return the lowest index in `iterable` where `value` is found.
    Returns ``-1`` if not found.

    Parameters
    ----------
    nw : yatel.db.YatelNetwork
        network source of data.
    iterable : iterator
        iterable object.
    value :
        Value to look for.
    start : int or None
        Starting point.
    end : int or None
        Finishing point.

    """
    try:
        if start is None and end is None:
            return iterable.index(value)
        if end is None:
            return iterable.index(value, start)
        return iterable.index(value, start, end)
    except:
        return -1


#==============================================================================
# DATE AND TIME
#==============================================================================

@qbjfunction()
def now(nw, *args, **kwargs):
    """Return the current local date and time."""
    return dt.datetime.now()


@qbjfunction()
def utcnow(nw, *args, **kwargs):
    """Return the current UTC date and time."""
    return dt.datetime.utcnow()


@qbjfunction()
def today(nw, *args, **kwargs):
    """Return the current local date."""
    return dt.date.today()


@qbjfunction()
def utctoday(nw, *args, **kwargs):
    """Return ``date`` object of current UTC date and time."""
    return dt.datetime.utcnow().date()


@qbjfunction()
def time(nw, *args, **kwargs):
    """Return ``time`` object of current local date and time.."""
    return dt.datetime.now().time()


@qbjfunction()
def utctime(nw, *args, **kwargs):
    """Return ``time`` object of current UTC date and time."""
    return dt.datetime.utcnow().time()


@qbjfunction
def get_from_time(nw, datetime_instance, dtformat, *args, **kwargs):
    """Return a ``str`` from a `datetime_instance` that is a ``datetime``
    object, according to specified format in `dtformat`.

    About `format https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior`_
    """
    return datetime_instance.strftime(dtformat)


#==============================================================================
# ARITMETICS
#==============================================================================

@qbjfunction()
def minus(nw, minuend, sust):
    """Return subtraction of `sust` from `minuend`."""
    return minuend - sust


@qbjfunction()
def times(nw, t0, t1):
    """Return multiplication of `t0` by `t1` """
    return t0 * t1


@qbjfunction()
def div(nw, dividend, divider):
    """Return division of `dividend` by `divider`."""
    return dividend / float(divider)


@qbjfunction()
def floor(nw, dividend, divider):
    """Return mod from division operation between `dividend` and
    `divider`."""
    return dividend % float(divider)


@qbjfunction()
def pow(nw, radix, exp):
    """Return exponentiation of `radix` to `exp`. """
    return radix ** exp


@qbjfunction()
def xroot(nw, radix, root):
    """Computes nth root with given `radix` and `root`."""
    return radix ** (1/float(root))


@qbjfunction()
def count(nw, iterable, to_count):
    """Returns the number of occurrences of `to_count` in `iterable`."""
    return collections.Counter(iterable)[to_count]


#==============================================================================
# STRING
#==============================================================================

@qbjfunction()
def split(nw, string, s=None, maxsplit=None):
    """Return a list of the words of `string`. With `s` as separator and
    maximum number of split by `maxsplit`.

    Parameters
    ----------

    string : str
        String to split.
    s : str ot None
        Used as separator if given, if ``None`` uses whitespace characters as
        separators.
    maxsplit : int or None
        Maximum number of split on `string` and the remainder of the string
        is returned as the final element of the list, if ``None`` no limit.
    """
    if s is None and maxsplit is None:
        return string.split()
    elif maxsplit is None:
        return string.split(s)
    return string.split(s, maxsplit)


@qbjfunction()
def rsplit(nw, string, s=None, maxsplit=None):
    """Return a list of the words of `string`, scanning `s` from the end. With
    `s` as separator and maximum number of split by `maxsplit`.

    Parameters
    ----------

    string : str
        String to split.
    s : str ot None
        Used as separator if given, if ``None`` uses whitespace characters as
        separators.
    maxsplit : int or None
        Maximum number of split on `string` and the remainder of the string
        is returned as the first element of the list, if ``None`` no limit.
    """
    if s is None and maxsplit is None:
        return string.rsplit()
    elif maxsplit is None:
        return string.rsplit(s)
    return string.rsplit(s, maxsplit)


@qbjfunction()
def strip(nw, string, chars=None):
    """Return a copy of `string` with leading and trailing characters
    removed. if `chars` is ``None`` whitespaces are removed otherwise the
    characters in the string will be stripped from the both ends.
    """
    if chars is None:
        return string.strip()
    return string.strip(chars)


@qbjfunction()
def lstrip(nw, string, chars=None):
    """Return a copy of `string` with leading characters removed. If
    `chars` is omitted or ``None``, whitespace characters are removed. If
    given and not ``None``, `chars` must be a string; the characters in the string
    will be stripped from the beginning of the string.
    """
    if chars is None:
        return string.lstrip()
    return string.lstrip(chars)


@qbjfunction()
def rstrip(nw, string, chars=None):
    """Return a copy of `string` with trailing characters removed. If
    `chars` is omitted or ``None``, whitespace characters are removed. If
    given and not ``None``, `chars` must be a string; the characters in the
    string will be stripped from the end of the string.
    """
    if chars is None:
        return string.rstrip()
    return string.rstrip(chars)


@qbjfunction()
def join(nw, joiner, to_join):
    """Concatenate a list or tuple of words with intervening occurrences of
    `joiner`.
    """
    return joiner.join(to_join)


@qbjfunction()
def upper(nw, string):
    """Return a copy of `string`, with lower case letters converted to
    upper case.
    """
    return string.upper()


@qbjfunction()
def lower(nw, string):
    """Return a copy of `string`, with upper case letters converted to
    lower case.
    """
    return string.lower()


@qbjfunction()
def title(nw, string):
    """Returns a copy of `string` in which first characters of all the words
    are capitalized.
    """
    return string.title()


@qbjfunction()
def capitalize(nw, string):
    """Return a copy of `string` with its first character capitalized and
    the rest lowercased.
    """
    return string.capitalize()


@qbjfunction()
def isalnum(nw, string):
    """Return true if all characters in `string` are alphanumeric and there
    is at least one character, false otherwise.
    """
    return string.isalnum()


@qbjfunction()
def isalpha(nw, string):
    """Return true if all characters in `string` are alphabetic and there is
    at least one character, false otherwise.
    """
    return string.isalpha()


@qbjfunction()
def isdigit(nw, string):
    """Return true if all characters in `string` are digits and there is at
    least one character, false otherwise.
    """
    return string.isdigit()


@qbjfunction()
def startswith(nw, string, prefix, start=None, end=None):
    """Return True if `string` starts with the `prefix`, otherwise return
    False. `prefix` can also be a tuple of prefixes to look for. With optional
    `start`, test `string` beginning at that position. With optional
    `end`, stop comparing string at that position.
    """
    if start is None and end is None:
        return string.startswith(prefix)
    if end is None:
        return string.startswith(prefix, start)
    return string.startswith(prefix, start, end)


@qbjfunction()
def endswith(nw, string, suffix, start=None, end=None):
    """Return True if `string` ends with the specified `suffix`, otherwise
    return False. `suffix` can also be a tuple of suffixes to look for. With
    optional `start`, test beginning at that position. With optional
    `end`, stop comparing at that position.
    """
    if start is None and end is None:
        return string.endswith(suffix)
    if end is None:
        return string.endswith(suffix, start)
    return string.endswith(suffix, start, end)


@qbjfunction()
def istitle(nw, string):
    """Return true if `string` is a titlecased string and there is at least
    one character."""
    return string.istitle()


@qbjfunction()
def isupper(nw, string):
    """Return ``true`` if all cased characters in `string` are uppercase and
    there is at least one cased character, ``false`` otherwise.
    """
    return string.isupper()


@qbjfunction()
def isspace(nw, string):
    """Return ``true`` if there are only whitespace characters in `string`
    and there is at least one character, ``false`` otherwise.
    """
    return string.isspace()


@qbjfunction()
def islower(nw, string):
    """Return ``true`` if all cased characters in `string` are lowercase and
    there is at least one cased character, ``false`` otherwise.
    """
    return string.islower()


@qbjfunction()
def swapcase(nw, string):
    """Return a copy of `string`, with lower case letters converted to upper
    case and vice versa.
    """
    return string.swapcase()


@qbjfunction()
def replace(nw, string, old, new, count=None):
    """Return a copy of `string` with all occurrences of `old` replaced by
    `new`. If `count` is given, the first `count` occurrences are
    replaced.
    """
    if count is None:
        return string.replace(old, new)
    return string.replace(old, new, count)


@qbjfunction()
def find(nw, string, subs, start=None, end=None):
    """Return the lowest index in `string` where the substring `sub` is
    found such that `sub` is wholly contained in ``string[start:end]``. Return -1 on
    failure. Defaults for `start` and `end` and interpretation of negative values
    is the same as for slices.
    """
    try:
        if start is None and end is None:
            return string.find(subs)
        if end is None:
            return string.find(subs, start)
        return string.find(subs, start, end)
    except:
        return -1


@qbjfunction()
def rfind(nw, string, subs, start=None, end=None):
    """Return the highest index in `string` where the substring `sub` is
    found.
    """
    try:
        if start is None and end is None:
            return string.rfind(subs)
        if end is None:
            return string.rfind(subs, start)
        return string.rfind(subs, start, end)
    except:
        return -1


# TODO: Regex, trigonometric, and math contants SUPPORT

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

