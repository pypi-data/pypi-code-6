#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Functions which allows to read serialized informations for autoparser.
"""
# Imports =====================================================================
import os.path
import copy

import yaml
import httpkie


# Functions & objects =========================================================
def _get_source(link):
    """
    Return source of the `link` whether it is filename or url.

    Args:
        link (str): Filename or URL.

    Returns:
        str: Content.

    Raises:
        UserWarning: When the `link` couldn't be resolved.
    """
    if link.startswith("http://") or link.startswith("https://"):
        down = httpkie.Downloader()
        return down.download(link)

    if os.path.exists(link):
        with open(link) as f:
            return f.read()

    raise UserWarning("html: '%s' is neither URL or data!" % link)


def _process_config_item(item, dirname):
    """
    Process one item from the configuration file, which contains multiple items
    saved as dictionary.

    This function reads additional data from the config and do some
    replacements - for example, if you specify url, it will download data
    from this url and so on.

    Args:
        item (dict): Item, which will be processed.

    Note:
        Returned data format::
            {
                "link": "link to html page/file",
                "html": "html code from file/url",
                "vars": {
                    "varname": {
                        "data": "matching data..",
                        ...
                    }
                }
            }

    Returns:
        dict: Dictionary in format showed above.
    """
    item = copy.deepcopy(item)
    html = item.get("html", None)

    if not html:
        raise UserWarning("Can't find HTML source for item:\n%s" % str(item))

    # process HTML link
    link = html if "://" in html else os.path.join(dirname, html)
    del item["html"]

    # replace $name with the actual name of the field
    for key, val in item.items():
        if "notfoundmsg" in val:
            val["notfoundmsg"] = val["notfoundmsg"].replace("$name", key)

    return {
        "html": _get_source(link),
        "link": link,
        "vars": item
    }


def read_config(file_name):
    """
    Read YAML file with configuration and pointers to example data.

    Args:
        file_name (str): Name of the file, where the configuration is stored.

    Returns:
        dict: Parsed and processed data (see :func:`_process_config_item`).

    Example YAML file::
        html: simple_xml.xml
        first:
            data: i wan't this
            required: true
            notfoundmsg: Can't find variable $name.
        second:
            data: and this
        ---
        html: simple_xml2.xml
        first:
            data: something wanted
            required: true
            notfoundmsg: Can't find variable $name.
        second:
            data: another wanted thing
    """
    dirname = os.path.dirname(
        os.path.abspath(file_name)
    )
    dirname = os.path.relpath(dirname)

    # create utf-8 strings, not unicode
    def custom_str_constructor(loader, node):
        return loader.construct_scalar(node).encode('utf-8')
    yaml.add_constructor(u'tag:yaml.org,2002:str', custom_str_constructor)

    config = []
    with open(file_name) as f:
        for item in yaml.load_all(f.read()):
            config.append(
                _process_config_item(item, dirname)
            )

    return config
