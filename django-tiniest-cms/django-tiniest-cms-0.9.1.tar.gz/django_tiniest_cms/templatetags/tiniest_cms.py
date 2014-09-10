import markdown

from django import template
from django.core.cache import cache

from django_tiniest_cms.models import Content


def content(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires an argument" % token.contents.split()[0]
        )
    if not (name[0] == name[-1] and name[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's name argument should be in quotes" % tag_name
        )
    name = name.strip('"\'')
    nodelist = parser.parse(('endcontent',))
    parser.delete_first_token()
    return ContentNode(nodelist, content_name=name)


class ContentNode(template.Node):
    def __init__(self, nodelist, content_name):
        self.nodelist = nodelist
        self.content_name = content_name

    def render(self, context):
        try:
            key = 'tiniest-content-{0}'.format(self.content_name)
            cached_content = cache.get(key)
            if cached_content is not None:
                content_html = cached_content
            else:
                content = Content.objects.get(name=self.content_name)
                content_html = markdown.markdown(
                    content.content,
                    output_format='html5',
                    safe_mode='escape'
                )
                cache.set(key, content_html, 3600)
            return content_html
        except Content.DoesNotExist:
            return self.nodelist.render(context)


register = template.Library()
register.tag('content', content)
