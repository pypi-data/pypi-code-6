""" Module for the global capabilities object

Named `structure` instead of `capabilities` to avoid import confusion between
object and module in root __init__.py
"""


def _flatten(to_flatten):
    """ Flatten nested dicts """
    result = []

    def _flatten_helper(to_flatten):
        # if it's a dict, go to the next level
        if isinstance(to_flatten, dict):
            for item in to_flatten.values():
                _flatten_helper(item)
        # otherwise, we're at the end
        else:
            result.append(to_flatten)

    _flatten_helper(to_flatten)
    return result


class _Capabilities(object):

    # the internal representation of nested dicts
    _internal = {}
    _already_loaded = False

    @classmethod
    def ensure_loaded(cls):
        """ Ensure the capabilities are loaded

        Must be called before accessing any data.
        Is idempotent.
        """
        # if we've already loaded this, don't do it again
        if cls._already_loaded:
            return

        # we use the short circuit to avoid doing this local import more than once
        loader.load()
        cls._already_loaded = True

    def _traverse(self, steps):
        """ Traversal of nested dicts using the given steps """

        self.ensure_loaded()

        return reduce(
            # traverse the nested dicts
            lambda current_dict, next_step: current_dict[next_step],
            # using the given steps
            steps,
            # start at our top-level dict
            self._internal
        )

    def __getitem__(self, name):
        """ Look up using the dot-separated name """

        steps = name.split('.')
        result = self._traverse(steps)
        # make sure our result is not a dict, that we're at the lowest level
        if isinstance(result, dict):
            raise KeyError("`{}` isn't a fully-qualified name".format(name))

        return result

    def __setitem__(self, name, value):
        """ Set a value using the dot-separated name """
        steps = name.split('.')

        # helper for creating dictionaries for the next step, if it doesn't exist
        def dict_creation_stepper(current_dict, next_step):
            if next_step not in current_dict:
                current_dict[next_step] = {}
            return current_dict[next_step]

        # go down to the second-to-last step; this is the last dict
        # the final step should store the value, rather than another dict
        lowest_dict = reduce(dict_creation_stepper, steps[:-1], self._internal)

        # store the value with the last step
        lowest_dict[steps[-1]] = value

    def __contains__(self, name):
        steps = name.split('.')
        try:
            self._traverse(steps)
        except KeyError:
            # if there is a key error while we traverse, then it is not 'in' this
            return False
        # if we make it without errors, it is 'in' this
        return True

    def group(self, search_prefix=''):
        """ Get a flat list of everything matching the search_prefix.

        Must be a dot-separated name or empty string. We traverse each
        dot-separated level. If a key doesn't exist, we return an empty list.
        Empty string means "everything."
        """

        self.ensure_loaded()

        if search_prefix == '':
            # in the special case, the dicts to collapse are just everything
            dicts = self._internal
        else:
            # split into steps
            steps = search_prefix.split('.')
            # if there is a key error while traversing, just return an empty list
            # for an empty query
            try:
                dicts = self._traverse(steps)
            except KeyError:
                return []

        # collapse all of the dicts all the way down
        return _flatten(dicts)


global capabilities
capabilities = _Capabilities()

# we need to import loader here to avoid a circular import
from . import loader
