
import tw2.core as twc
import tw2.jquery.base as twjq_c
import defaults

fancytree_js = twjq_c.jQueryPluginJSLink(
    name=defaults._fancytree_name_,
    version=defaults._fancytree_version_,
    #variant='min',
    modname='tw2.jqplugins.fancytree',
    subdir = '',
)

fancytree_css = twjq_c.jQueryPluginCSSLink(
    name=defaults._fancytree_name_,
    version = defaults._fancytree_version_,
    modname = 'tw2.jqplugins.fancytree',
    #subdir = 'skin-bootstrap',
    subdir = 'skin-vista',
)

__all__ = ['fancytree_js', 'fancytree_css']
