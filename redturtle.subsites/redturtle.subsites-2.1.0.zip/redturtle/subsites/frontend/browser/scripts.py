# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.PythonScripts.standard import url_quote

from Products.ResourceRegistries.browser.scripts import ScriptsView as BaseScriptsView
from plone.app.layout.navigation.root import getNavigationRoot


class ScriptsView(BaseScriptsView):
    """ Information for script rendering. """

    def _getRegistryURL(self, registry):
        """Service method to get the right registry URL.
        This is constructed with the "/subsite" section if we are in a subsite enrironment.
        """
        subsite_path = getNavigationRoot(self.context)
        brains = self.context.portal_catalog(path={'query':subsite_path, 'depth':0})
        if brains:
            subsite = brains[0]
            registry_url = subsite.getURL() + '/portal_javascripts'
        else:
            registry_url = registry.absolute_url()
        return registry_url

    def scripts(self):
        registry = self.registry()
        registry_url = self._getRegistryURL(registry)
        context = aq_inner(self.context)

        scripts = registry.getEvaluatedResources(context)
        skinname = url_quote(self.skinname())
        result = []
        for script in scripts:
            inline = bool(script.getInline())
            if inline:
                content = registry.getInlineResource(script.getId(), context)
                data = {'inline': inline,
                        'conditionalcomment' : script.getConditionalcomment(),
                        'content': content}
            else:
                if script.isExternalResource():
                    src = "%s" % (script.getId(),)
                else:
                    src = "%s/%s/%s" % (registry_url, skinname, script.getId())
                data = {'inline': inline,
                        'conditionalcomment' : script.getConditionalcomment(),
                        'src': src}
            result.append(data)
        return result
