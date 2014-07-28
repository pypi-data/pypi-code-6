from zope import interface, component
from raptus.article.core import interfaces


class NamedDefaultComponent(object):
    """ Provider to define a default component using a named adapter
    """
    interface.implements(interfaces.INamedDefaultComponent)
    component.adapts(interfaces.IArticle)

    def __init__(self, context):
        self.context = context


def SetDefaults(object, event):
    """ Sets the default components defined by the registered adapters providing IDefaultComponents
    """
    for name, provider in component.getAdapters((object,),
                                                interfaces.IDefaultComponents):
        for comp in provider.getComponents():
            interface.alsoProvides(object, comp.interface)
    for name, provider in component.getAdapters((object,),
                                                interfaces.INamedDefaultComponent):
        comp = component.queryAdapter(object,
                                      interface=interfaces.IComponent,
                                      name=name)
        if comp is not None:
            interface.alsoProvides(object, comp.interface)
    object.reindexObject(idxs=['object_provides'])
