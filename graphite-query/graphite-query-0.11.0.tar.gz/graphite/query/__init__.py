""" This is a modified version of package render from graphite-web """
import pytz
from graphite import settings
from graphite.settings import setup_storage_variables
from graphite.query.evaluator import evaluateTarget
from graphite.query.attime import parseATTime
import tzlocal

def query(*args, **kwargs):
    """ Returns a list of graphite.query.datalib.TimeSeries instances

        `query` takes both positional and keyword arguments, which in turn are taken
        from [graphite-web's render API]
        (http://graphite.readthedocs.org/en/latest/render_api.html)
        except for the graph/format arguments, which are, of course,
        inapplicable to graphite-query.

        In short, its parameters (in positional order) are:

        * `target`: required, a `graphite-web` compatible path (i.e. string), or a `list` of
         paths, see <http://graphite.readthedocs.org/en/latest/render_api.html#target>
         for additional documentation.
        * `from` and `until`: two optional parameters that specify the relative or
         absolute time period to graph.
         see <http://graphite.readthedocs.org/en/latest/render_api.html#from-until>
        * `tz`: optional, time zone to convert all times into.
         If this parameter is not specified, then `graphite.query.settings.TIME_ZONE`
         is used (if any).  Finally, system's timezone is used if `TIME_ZONE` is empty.
         see <http://graphite.readthedocs.org/en/latest/render_api.html#tz>
    """
    params = {}

    try:
        params['target'] = args[0]
    except IndexError:
        pass

    try:
        params['from'] = args[1]
    except IndexError:
        pass

    try:
        params['until'] = args[2]
    except IndexError:
        pass

    try:
        params['tz'] = args[3]
    except IndexError:
        pass

    params.update(kwargs)

    if kwargs.has_key('from_'):
        params['from'] = kwargs['from_']

    if kwargs.has_key('from_time'):
        params['from'] = kwargs['from_time']

    try:
        tzinfo = pytz.timezone(settings.TIME_ZONE)
    except AttributeError:
        tzinfo = tzlocal.get_localzone()
    if 'tz' in params:
        try:
            tzinfo = pytz.timezone(params['tz'])
        except pytz.UnknownTimeZoneError:
            pass
    params['tzinfo'] = tzinfo

    if 'until' in params:
        untilTime = parseATTime(params['until'], tzinfo)
    else:
        untilTime = parseATTime('now', tzinfo)
    if 'from' in params:
        fromTime = parseATTime(params['from'], tzinfo)
    else:
        fromTime = parseATTime('-1d', tzinfo)
    startTime = min(fromTime, untilTime)
    endTime = max(fromTime, untilTime)
    assert startTime < endTime, "Invalid empty time range"

    params['startTime'] = startTime
    params['endTime'] = endTime

    data = []
    if isinstance(params['target'], basestring):
        data.extend(evaluateTarget(params, params['target']))
    elif isinstance(params['target'], list):
        for target in params['target']:
            data.extend(evaluateTarget(params, target))
    else:
        raise TypeError("The target parameter must be a string or a list")

    return data

def eval_qs(query_string):
    """ A helper function that converts a ``graphite-web`` compatible
        URL query string (compatible with the render controller)
        and then calls the ``query`` function to get the result.
    """
    from urlparse import parse_qs

    params = parse_qs(query_string)

    # In parse_qs every value is a list, so we convert
    # them to strings
    for key, value in params.items():
        if key != "target":
            params[key] = value[0]
    return query(**params)

def get_all_leaf_nodes():
    """Return a ``list`` of all leaf nodes/targets that are found in the
    ``settings.STORAGE_DIR``"""
    from graphite.storage import get_finder, FindQuery
    from graphite.node import LeafNode

    finders = [get_finder(finder_path)
                       for finder_path in settings.STORAGE_FINDERS]
    # Go iteratively through the patern "*.*.*......."
    # and, after some time, return all available nodes.
    # Might be also done just by going through the directory
    # structure?
    res = []
    pattern = "*"
    found = True
    while found:
        found = False
        for finder in finders:
            for node in finder.find_nodes(FindQuery(pattern, None, None)):
                found = True
                if isinstance(node, LeafNode):
                    res.append(node.path)
        pattern += ".*"
    return res