from xml.dom.minidom import parse
from optparse import OptionParser
from jinja2 import Environment, PackageLoader

def attribute2param(element):
    params={}
    attributes = element.attributes.items()
    for attribute in attributes:
        params[attribute[0]] = attribute[1]
    return params

def get_table_header(chaine):
    header = chaine.split("\n")[0]
    retour =  header.split(',')
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

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="inputfile",
            help="Screen Input File", metavar="FILE")
    parser.add_option("-s", "--screen", dest="inputscreen",
            help="Screen Input", metavar="Name")

    (options, args) = parser.parse_args()

    # Chargement de l'environnement pour les templates
    env = Environment(loader = PackageLoader('screen2html', 'templates'))
    env.filters['get_table_header'] = get_table_header
    env.filters['get_table_lignes'] = get_table_lignes
    env.filters['get_table_ligne_value'] = get_table_ligne_value

    screen_name = options.inputscreen
    screen = parse('%s.screen' % screen_name)
    htmlscreen = open('%s.html' % screen_name, 'w')

    page = env.get_template('page.tpl')

    content = ''
    root = screen.childNodes[0]
    widgets = root.childNodes
    for widget in widgets:
        if widget.nodeName == u'widgets' :
            subcontent=''
            template_path = widget.getAttribute('xsi:type')
            if template_path == 'model:Master':
                screens = widget.childNodes
                overrides={}
                if hasoverride(widget):
                    subwidgets = widget.getElementsByTagName('widgets')
                    for subwidget in subwidgets:
                        if subwidget.hasChildNodes:
                            subitems = subwidget.getElementsByTagName('items')
                            subelements = {}
                            for subitem in subitems:
                                subelements[subitem.getAttribute('ref')] = attribute2param(subitem)
                        params = attribute2param(subwidget)
                        params['subitems']=subelements
                        overrides['ref_%s' % subwidget.getAttribute('ref')] = params 
                        print overrides
                for screen in screens:
                    if screen.nodeName == u'screen':
                        subscreen = env.get_template('%s.tpl' % screen.getAttribute('href').replace("#","/"))
                        subcontent = subscreen.render(overrides)

            subtemplate = env.get_template('%s.tpl' % template_path.replace(":","/"))
            content += subtemplate.render(
                    attribute2param(widget),
                    content=subcontent
                       )


    htmlscreen.write(page.render(page_title=screen_name, content=content))
