from django import template
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from base64 import b64encode as encode


register = template.Library()


class SkelNode(template.Node):

    def __init__(self, skeleton, path):
        self.skeleton = skeleton
        self.path = path

    def render(self, context):
        skel = self.skeleton.resolve(context)
        path = self.path.resolve(context) if self.path else self.path
        t = get_template(skel)

        # get HTML renderer
        request = context['request']

        # render facet
        renderer = request.html_renderer
        facet = renderer.render(path, t.render(context))

        #api = request.studiogdo_api
        #response = api.post_facet(encode(path), t.render(context), 'dom5')
        #facet = unicode(response.content, 'utf-8')

        # set trace
        if context['studiogdo_debug']:
            return mark_safe("<!-- start %s (%s)-->\n" % (skel, path) + facet + "<!-- end %s -->\n" % skel)

        return mark_safe(facet)


@register.tag
def skel(parser, token):
    contents = token.split_contents()
    if len(contents) != 3:
        raise template.TemplateSyntaxError('skel needs at 2 arguments')
    else:
        skeleton = parser.compile_filter(contents[1])
        path = parser.compile_filter(contents[2])
        return SkelNode(skeleton, path)


@register.filter
def b64encode(value):
    return encode(value)
