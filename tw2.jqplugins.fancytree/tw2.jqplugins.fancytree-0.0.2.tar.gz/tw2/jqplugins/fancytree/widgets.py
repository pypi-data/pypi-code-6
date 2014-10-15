"""
 see http://wwwendt.de/tech/fancytree/demo/
 http://wwwendt.de/tech/fancytree/demo/sample-api.html
 for examples of the FancyTree API
"""
import tw2.core as twc
#from tw2.core.resources import encoder
from tw2.core.js import js_function, js_callback
import tw2.jquery
import tw2.jqplugins.ui.base as tw2_jq_ui

import base


class FancyTreeWidget(tw2_jq_ui.JQueryUIWidget):

    resources = [
        tw2.jquery.jquery_js,
        tw2_jq_ui.jquery_ui_js,
        tw2_jq_ui.jquery_ui_css,
        base.fancytree_js,
        base.fancytree_css,
    ]

    template = "tw2.jqplugins.fancytree.templates.fancytree"

    selector = twc.Variable("Escaped id. jQuery selector.")
    options = twc.Param("Config. options to pass to fancytree", default={})

    def prepare(self):
        if 'id' in self.attrs:
            self.selector = "#" + self.attrs['id'].replace(':', '\\:')

        self.add_call(js_function("$(document).ready")(js_callback(
            tw2.jquery.jQuery(self.selector).fancytree(self.options)
        )))
        super(FancyTreeWidget, self).prepare()
