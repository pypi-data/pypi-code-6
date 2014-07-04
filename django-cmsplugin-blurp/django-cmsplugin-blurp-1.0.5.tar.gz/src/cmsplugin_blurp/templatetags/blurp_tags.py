from django import template

from classytags.arguments import Argument
from classytags.core import Options, Tag

from .. import utils

register = template.Library()

@register.tag
class RenderBlurp(Tag):
    name = 'render_blurp'
    options = Options(
        Argument('name', resolve=False),
    )


    def render_tag(self, context, name):
        renderer = utils.resolve_renderer(name)
        if not renderer:
            return ''
        template = renderer.render_template()
        context = renderer.render(context)
        if not hasattr(template, 'render'):
            template = template.Template(template)
        return template.render(context)

@register.tag
class BlurpNode(Tag):
    '''Insert content generated from a blurp block and render inside template'''
    name = 'blurp'
    options = Options(
            Argument('name'),
            blocks=[('endblurp', 'nodelist')])

    def render_tag(self, context, name, nodelist):
        context.push()
        utils.insert_blurp_in_context(name, context)
        output = self.nodelist.render(context)
        context.pop()
        return output
