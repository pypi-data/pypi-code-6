''' module supporting yaml-format configuration files '''
# copyright (c) 2014, Edward F. Wahl.

from bunch import Bunch
import os.path
import yaml

def _bunchify_tree(tree):
    '''
    convenience function to traverse a tree of dicts, lists
    and turn all dicts it contains to bunches
    '''
    if isinstance(tree, dict):
        tree = Bunch(tree)
        for item in tree:
            tree[item] = _bunchify_tree(tree[item])
    elif isinstance(tree, list):
        for idx, item in enumerate(tree):
            tree[idx] = _bunchify_tree(item)

    return tree

def load(yaml_data, **kwargs):
    ''' convert yaml data into a configuration
         @param yaml_data: yaml data to be parsed
         @param configData: do substitution from this data

         parsing includes two custom yaml tags

         !format does string.format substitution using mapping data in
         the node. kwargs override default values if present
    '''

    def _python_format(loader, node):
        ''' do python string formatting

            requires a mapping input
            special key "format" is the string to be formatted
            all other keys are passed as keyword arguments
        '''

        params = Bunch(loader.construct_mapping(node))

        # allow kwargs substitution
        for key, value in kwargs.items():
            if key in params:
                params[key] = value

        rv = params.format.format(**params) #pylint: disable=W0142
        return rv

    yaml.add_constructor('!format', _python_format)

    return _bunchify_tree(yaml.load(yaml_data))

def load_file(path, **kwargs):
    ''' convert yaml data into a configuration
         @param path: path to file to be parsed
         @return:

         wrapper around the config_to_yaml function
         see details of that function for operation
    '''

    return load(open(os.path.expanduser(path), 'r').read(), **kwargs)

