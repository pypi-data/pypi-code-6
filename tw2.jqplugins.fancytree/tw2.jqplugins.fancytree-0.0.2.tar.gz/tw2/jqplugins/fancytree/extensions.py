'''
Makes the extension libraries available for use in FancyTree widgets

Example usage of widget definition with extensions added:

	from tw2.jqplugins.fancytree import FancyTreeWidget
	from tw2.jqplugins.fancytree.extensions import ext_contextmenu
	
	class DemoFancyTreeWidget(FancyTree):		
		resources = [context_menu.ResourceBundle]
		options = { ... }

''' 
import defaults
import tw2.core as twc
from tw2.core.resources import ResourceBundle


pth = 'static/jquery/plugins/fancytree/3rd-party/extensions/'

ext_contextmenu_js = twc.JSLink(
	modname ='tw2.jqplugins.fancytree', 
    filename = pth + 'contextmenu/js/jquery.contextMenu-1.6.5.js'
)

ext_contextmenu_js_ = twc.JSLink(
	modname ='tw2.jqplugins.fancytree', 
    filename = pth + 'contextmenu/js/jquery.fancytree.contextMenu.js'
)

ext_contextmenu_css = twc.CSSLink(
	modname ='tw2.jqplugins.fancytree', 
    filename = pth + 'contextmenu/css/jquery.contextMenu.css'
)

ext_contextmenu_imgs = twc.DirLink(
	modname ='tw2.jqplugins.fancytree', 
	filename = pth + 'contextmenu/images'
)

#ext_contextmenu = ResourceBundle(
#	resources=[
#    	ext_contextmenu_js, 
#		ext_contextmenu_css, 
#	    ext_contextmenu_imgs
#	])

# ext_hotkeys ...

#__all__ = [ext_contextmenu]
