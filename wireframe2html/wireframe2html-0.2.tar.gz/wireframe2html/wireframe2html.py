import re
from xml.dom.minidom import parse
from optparse import OptionParser
from jinja2 import Environment, PackageLoader
from types import NoneType


def mreplace(replacements, text):
    regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
    return regex.sub(lambda mo: replacements[mo.string[mo.start():mo.end()]], text)


def attribute2param(element):
    params = {}
    attributes = element.attributes.items()
    for attribute in attributes:
        params[attribute[0]] = attribute[1]
    return params


def get_table_header(chaine):
    header = chaine.split("\n")[0]
    retour = header.split(',')
    return retour


def get_table_lignes(chaine):
    lignes = chaine.split("\n")[1:]
    return lignes


def get_table_ligne_value(chaine):
    values = chaine.split(',')
    return values


def hasoverride(element):
    childs = element.childNodes
    retour = False
    for child in childs:
        if child.nodeName == u'overrides':
            retour = True
    return retour


def handleModelScreen(document, env):
    widgets = document.childNodes
    content = ''
    for widget in widgets:
        if widget.nodeName == u'widgets':
            content += handleWidgets(widget, env)
    return content


def handleWidgets(widget,env):
    content = ''
    if widget.getAttribute('xsi:type') == 'model:Master':
        overrides = []
        if hasoverride(widget):
            overrides = handleOverrides(widget.getElementsByTagName('overrides'))
        subcontent = handleScreen(widget.getElementsByTagName('screen'), env, overrides)
        template_path = widget.getAttribute('xsi:type')
        subtemplate = env.get_template('%s.tpl' % template_path.replace(":", "/"))
        content += subtemplate.render(
                    attribute2param(widget),
                    content=subcontent
                       )
    return content

def handleScreen(screens, env, overrides = []):
    if overrides is None:
        overrides=[]
    subcontent = ''
    for screen in screens:
        if screen.nodeName == u'screen':
            screen_path = mreplace({'#':'/','&':'_'}, screen.getAttribute('href')).replace("%20", "")
            subscreen = env.get_template('%s.tpl' % screen_path)
            subcontent = subscreen.render(overrides)
    return subcontent

def handleOverrides(data):
    overrides = {}
    subWidgets = data[0].getElementsByTagName('widgets')
    for subWidget in subWidgets:
        handleWidgetOverrides(subWidget)
        overrides['ref_%s' % subWidget.getAttribute('ref')] = handleWidgetOverrides(subWidget)
    return overrides

def handleWidgetOverrides(widgetoverride):
    params = attribute2param(widgetoverride)
    params['subitems'] = handleItems(widgetoverride)
    return params

def handleItems(widget):
    subitems = widget.getElementsByTagName('items')
    subelements = {}
    for subitem in subitems:
        subelements[subitem.getAttribute('ref')] = attribute2param(subitem)
    return subelements 

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="inputfile",
            help="Screen Input File", metavar="FILE")
    parser.add_option("-s", "--screen", dest="inputscreen",
            help="Screen Input", metavar="Name")
    parser.add_option("-w", "--workspace", dest="workspace",
            help="Wireframesketcher workspace", metavar="Workspace")
    parser.add_option("-o", "--output", dest="outputDir",
            help="Output Dir", metavar="Directory")

    (options, args) = parser.parse_args()

    # Chargement de l'environnement pour les templates
    env = Environment(loader=PackageLoader('wireframe2html', 'templates'))
    env.filters['get_table_header'] = get_table_header
    env.filters['get_table_lignes'] = get_table_lignes
    env.filters['get_table_ligne_value'] = get_table_ligne_value

    screen_name = options.inputscreen
    screen = parse('%s.screen' % screen_name)
    htmlscreen = open('%s.html' % screen_name, 'w')

    page = env.get_template('page.tpl')

    root = screen.childNodes[0]
    content = handleModelScreen(root, env)
    htmlscreen.write(page.render(page_title=screen_name, content=content))
