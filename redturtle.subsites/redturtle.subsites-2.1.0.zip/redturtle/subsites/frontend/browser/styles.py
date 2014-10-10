# -*- coding: utf-8 -*-

from Products.PythonScripts.standard import url_quote

from Products.ResourceRegistries.browser.styles import StylesView as BaseStylesView
from plone.app.layout.navigation.root import getNavigationRoot


class StylesView(BaseStylesView):
    """ Information for style rendering for a specific subsite section """

    def _getRegistryURL(self, registry):
        """Service method to get the right registry URL.
        This is constructed with the "/subsite" section if we are in a subsite enrironment.
        """
        subsite_path = getNavigationRoot(self.context)
        brains = self.context.portal_catalog(path={'query':subsite_path, 'depth':0})
        if brains:
            subsite = brains[0]
            registry_url = subsite.getURL() + '/portal_css'
        else:
            registry_url = registry.absolute_url()
        return registry_url

    def styles(self):
        registry = self.registry()
        registry_url = self._getRegistryURL(registry)

        styles = registry.getEvaluatedResources(self.context)
        skinname = url_quote(self.skinname())
        result = []
        for style in styles:
            rendering = style.getRendering()
            if rendering == 'link':
                src = "%s/%s/%s" % (registry_url, skinname, style.getId())
                data = {'rendering': rendering,
                        'media': style.getMedia(),
                        'rel': style.getRel(),
                        'title': style.getTitle(),
                        'conditionalcomment' : style.getConditionalcomment(),
                        'src': src}
            elif rendering == 'import':
                src = "%s/%s/%s" % (registry_url, skinname, style.getId())
                data = {'rendering': rendering,
                        'media': style.getMedia(),
                        'conditionalcomment' : style.getConditionalcomment(),
                        'src': src}
            elif rendering == 'inline':
                content = registry.getInlineResource(style.getId(),
                                                     self.context)
                data = {'rendering': rendering,
                        'media': style.getMedia(),
                        'conditionalcomment' : style.getConditionalcomment(),
                        'content': content}
            else:
                raise ValueError, "Unkown rendering method '%s' for style '%s'" % (rendering, style.getId())
            result.append(data)
        return result
