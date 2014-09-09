#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module contains number of template generators, which generates all the
python code for the parser.
"""
# Imports =====================================================================
import inspect

import utils
import conf_reader
import path_patterns


# Variables ===================================================================
IND = "    "  #: Indentation.


# Functions & objects =========================================================
def _index_idiom(el_name, index, alt=None):
    """
    Generate string where `el_name` is indexed by `index` if there are enough
    items or `alt` is returned.

    Args:
        el_name (str): Name of the `container` which is indexed.
        index (int): Index of the item you want to obtain from container.
        alt (whatever, default None): Alternative value.

    Returns:
        str: Python code.

    Live example::
        >>> import generator as g
        >>> print g._index_idiom("xex", 0)
            # pick element from list
            xex = xex[0] if xex else None
        >>> print g._index_idiom("xex", 1, "something")
        # pick element from list
        xex = xex[1] if len(xex) - 1 >= 1 else 'something'
    """
    el_index = "%s[%d]" % (el_name, index)

    if index == 0:
        cond = "%s" % el_name
    else:
        cond = "len(%s) - 1 >= %d" % (el_name, index)

    output = IND + "# pick element from list\n"

    return output + IND + "%s = %s if %s else %s\n\n" % (
        el_name,
        el_index,
        cond,
        repr(alt)
    )


def _required_idiom(tag_name, index, notfoundmsg):
    """
    Generate code, which make sure that `tag_name` has enoug items.

    Args:
        tag_name (str): Name of the container.
        index (int): Index of the item you want to obtain from container.
        notfoundmsg (str): Raise :class:`.UserWarning` with debug data and
                           following message.

    Returns:
        str: Python code.
    """
    cond = ""
    if index > 0:
        cond = " or len(el) - 1 < %d" % index

    tag_name = str(tag_name)

    output = IND + "if not el%s:\n" % cond
    output += IND + IND + "raise UserWarning(\n"
    output += IND + IND + IND + "%s +\n" % repr(notfoundmsg.strip() + "\n")
    output += IND + IND + IND + repr("Tag name: " + tag_name) + " + '\\n' +\n"
    output += IND + IND + IND + "'El:' + str(el) + '\\n' +\n"
    output += IND + IND + IND + "'Dom:' + str(dom)\n"
    output += IND + IND + ")\n\n"

    return output + IND + "el = el[%d]\n\n" % index


# parser template generators ##################################################
def _find_template(parameters, index, required=False, notfoundmsg=None):
    """
    Generate ``.find()`` call for HTMLElement.

    Args:
        parameters (list): List of parameters for ``.find()``.
        index (int): Index of the item you want to get from ``.find()`` call.
        required (bool, default False): Use :func:`_required_idiom` to returned
                 data.
        notfoundmsg (str, default None): Message which will be used for
                    :func:`_required_idiom` if the item is not found.

    Returns:
        str: Python code.

    Live example::
        >>> print g._find_template(["<xex>"], 3)
            el = dom.find('<xex>')
            # pick element from list
            el = el[3] if len(el) - 1 >= 3 else None
    """
    output = IND + "el = dom.find(%s)\n\n" % repr(parameters)[1:-1]

    if required:
        return output + _required_idiom(parameters[0], index, notfoundmsg)

    return output + _index_idiom("el", index)


def _wfind_template(use_dom, parameters, index, required=False,
                                                notfoundmsg=None):
    """
    Generate ``.wfind()`` call for HTMLElement.

    Args:
        use_dom (bool): Use ``dom`` as tag name. If ``False``, ``el`` is used.
        parameters (list): List of parameters for ``.wfind()``.
        index (int): Index of the item you want to get from ``.wfind()`` call.
        required (bool, default False): Use :func:`_required_idiom` to returned
                 data.
        notfoundmsg (str, default None): Message which will be used for
                    :func:`_required_idiom` if the item is not found.

    Returns:
        str: Python code.

    Live example::
        >>> print g._wfind_template(True, ["<xex>"], 3)
            el = dom.wfind('<xex>').childs
            # pick element from list
            el = el[3] if len(el) - 1 >= 3 else None
    """
    tag_name = "dom" if use_dom else "el"
    output = IND + "el = %s.wfind(%s).childs\n\n" % (
        tag_name,
        repr(parameters)[1:-1]
    )

    if required:
        return output + _required_idiom(parameters[0], index, notfoundmsg)

    return output + _index_idiom("el", index)


def _match_template(parameters, index, required=False, notfoundmsg=None):
    """
    Generate ``.match()`` call for HTMLElement.

    Args:
        parameters (list): List of parameters for ``.match()``.
        index (int): Index of the item you want to get from ``.match()`` call.
        required (bool, default False): Use :func:`_required_idiom` to returned
                 data.
        notfoundmsg (str, default None): Message which will be used for
                    :func:`_required_idiom` if the item is not found.

    Returns:
        str: Python code.

    Live example::
        >>> print g._match_template(["<xex>"], 3)
            el = dom.match('<xex>')
            # pick element from list
            el = el[3] if len(el) - 1 >= 3 else None
    """
    output = IND + "el = dom.match(%s)\n\n" % repr(parameters)[1:-1]

    #TODO: reduce None parameters

    if required:
        return output + _required_idiom(parameters[0], index, notfoundmsg)

    return output + _index_idiom("el", index)


def _neigh_template(parameters, index, left=True, required=False,
                                                  notfoundmsg=None):
    """
    Generate neighbour matching call for HTMLElement, which returns only
    elements with required neighbours.

    Args:
        parameters (list): List of parameters for ``.match()``.
        index (int): Index of the item you want to get from ``.match()`` call.
        left (bool, default True): Look for neigbour in the left side of el.
        required (bool, default False): Use :func:`_required_idiom` to returned
                 data.
        notfoundmsg (str, default None): Message which will be used for
                    :func:`_required_idiom` if the item is not found.

    Returns:
        str: Python code.
    """
    fn_string = "has_neigh(%s, left=%s)" % (
        repr(parameters.fn_params)[1:-1],
        repr(left)
    )

    output = IND + "el = dom.find(\n"
    output += IND + IND + "%s,\n" % repr(parameters.tag_name)

    if parameters.params:
        output += IND + IND + "%s,\n" % repr(parameters.params)

    output += IND + IND + "fn=%s\n" % fn_string
    output += IND + ")\n\n"

    if required:
        return output + _required_idiom(
            parameters.fn_params[0],
            index,
            notfoundmsg
        )

    return output + _index_idiom("el", index)

# /parser template generators #################################################


def _get_parser_name(var_name):
    """
    Parser name composer.

    Args:
        var_name (str): Name of the variable.

    Returns:
        str: Parser function name.
    """
    return "get_%s" % var_name


def _generate_parser(name, path, required=False, notfoundmsg=None):
    """
    Generate parser named `name` for given `path`.

    Args:
        name (str): Basename for the parsing function (see
                    :func:`_get_parser_name` for details).
        path (obj): :class:`.PathCall` or :class:`.Chained` instance.
        required (bool, default False): Use :func:`_required_idiom` to returned
                 data.
        notfoundmsg (str, default None): Message which will be used for
                    :func:`_required_idiom` if the item is not found.

    Returns:
        str: Python code for parsing `path`.
    """
    output = "def %s(dom):\n" % _get_parser_name(name)

    dom = True  # used specifically in _wfind_template
    parser_table = {
        "find": lambda path:
            _find_template(path.params, path.index, required, notfoundmsg),
        "wfind": lambda path:
            _wfind_template(
                dom,
                path.params,
                path.index,
                required,
                notfoundmsg
            ),
        "match": lambda path:
            _match_template(path.params, path.index, required, notfoundmsg),
        "left_neighbour_tag": lambda path:
            _neigh_template(
                path.params,
                path.index,
                True,
                required,
                notfoundmsg
            ),
        "right_neighbour_tag": lambda path:
            _neigh_template(
                path.params,
                path.index,
                False,
                required,
                notfoundmsg
            ),
    }

    if isinstance(path, path_patterns.PathCall):
        output += parser_table[path.call_type](path)
    elif isinstance(path, path_patterns.Chained):
        for path in path.chain:
            output += parser_table[path.call_type](path)
            dom = False
    else:
        raise UserWarning(
            "Unknown type of path parameters! (%s)" % str(path)
        )

    output += IND + "return el\n"
    output += "\n\n"

    return output


def _unittest_template(config):
    """
    Generate unittests for all of the generated code.

    Args:
        config (dict): Original configuration dictionary. See
               :mod:`~harvester.autoparser.conf_reader` for details.

    Returns:
        str: Python code.
    """
    output = "def test_parsers():\n"

    links = dict(map(lambda x: (x["link"], x["vars"]), config))

    for link in links.keys():
        output += IND + "# Test parsers against %s\n" % link
        output += IND + "html = handle_encodnig(\n"
        output += IND + IND + "_get_source(%s)\n" % repr(link)
        output += IND + ")\n"
        output += IND + "dom = dhtmlparser.parseString(html)\n"
        output += IND + "dhtmlparser.makeDoubleLinked(dom)\n\n"

        for var in links[link]:
            content = links[link][var]["data"].strip()

            output += IND + "%s = %s(dom)\n" % (var, _get_parser_name(var))

            if "\n" in content:
                output += IND
                output += "assert %s.getContent().strip().split() == %s" % (
                    var,
                    repr(content.split())
                )
            else:
                output += IND + "assert %s.getContent().strip() == %s" % (
                    var,
                    repr(content)
                )

            output += "\n\n"

    return output + "\n"


def generate_parsers(config, paths):
    """
    Generate parser for all `paths`.

    Args:
        config (dict): Original configuration dictionary used to get matches
                       for unittests. See
                       :mod:`~harvester.autoparser.conf_reader` for details.
        paths (dict): Output from :func:`.select_best_paths`.

    Returns:
        str: Python code containing all parsers for `paths`.
    """
    output = """#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# HTML parser generated by Autoparser
# (https://github.com/edeposit/edeposit.amqp.harvester)
#
import os
import os.path

import httpkie
import dhtmlparser


# Utilities
"""
    # add source of neighbour picking functions from utils.py
    output += inspect.getsource(conf_reader._get_source) + "\n\n"
    output += inspect.getsource(utils._get_encoding) + "\n\n"
    output += inspect.getsource(utils.handle_encodnig) + "\n\n"
    output += inspect.getsource(utils.is_equal_tag) + "\n\n"
    output += inspect.getsource(utils.has_neigh) + "\n\n"
    output += "# Generated parsers\n"

    for name, path in paths.items():
        path = path[0]  # pick path with highest priority

        required = config[0]["vars"][name].get("required", False)
        notfoundmsg = config[0]["vars"][name].get("notfoundmsg", "")

        output += _generate_parser(name, path, required, notfoundmsg)

    output += "# Unittest\n"
    output += _unittest_template(config)

    output += "# Run tests of the parser\n"
    output += "if __name__ == '__main__':\n"
    output += IND + "test_parsers()"

    return output
