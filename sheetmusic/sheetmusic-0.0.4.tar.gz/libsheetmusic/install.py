import os
import re
import subprocess

import lxml.etree

import libsheetmusic.main as main
import libsheetmusic.plugin_template as templates

def get_plugin_xml():
    plugin = lxml.etree.fromstring(templates.plugin_xml)
    functions = plugin.xpath('//functions')[0]
    for name in main.functions().keys():
        functions.insert(0, lxml.etree.Element('function', attrib = {'name': name}))
    return lxml.etree.tostring(plugin)

def get_version(system = os.system):
    proc = subprocess.Popen(['gnumeric', '--version'], stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    version = re.match(r"^gnumeric version '([0-9.]+)'.*", out).group(1)
    return version

def install(os = os):
    directory = os.path.expanduser('~/.gnumeric/%s/plugins/sheetmusic' % get_version(os.system))
    try:
        os.makedirs(directory)
    except OSError:
        pass

    plugin_xml = os.path.join(directory, 'plugin.xml')
    sheetmusic_py = os.path.join(directory, 'sheetmusic.py')

    with open(plugin_xml, 'w') as fp:
        fp.write(get_plugin_xml())

    with open(sheetmusic_py, 'w') as fp:
        fp.write(templates.sheetmusic_py)
