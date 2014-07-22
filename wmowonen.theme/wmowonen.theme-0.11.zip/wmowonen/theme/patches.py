from cgi import escape
from Acquisition import aq_inner
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from plonetheme.gov.browser.gov_folder_view import GovFolderView
from collective.contentleadimage.browser.viewlets import LeadImageViewlet
from Products.CMFCore import permissions
from Products.Archetypes.Field import ImageField

def tag(self, obj, css_class='tileImage'):
    context = aq_inner(obj)
    field = context.getField(IMAGE_FIELD_NAME)
    if field is not None:
        if field.get_size(context) != 0:
            scale = self.prefs.desc_scale_name
            try:
                return field.tag(context, scale=scale, css_class=css_class)
            except:
                return ''
    return ''

GovFolderView.tag = tag


# We patch the render of the leadimage viewlet to also show it for News Items
# the .pt is also overridden
def render(self):
    context = aq_inner(self.context)
    portal_type = getattr(context, 'portal_type', None)
    allowed_types = list(self.prefs.allowed_types)
    allowed_types.append('News Item')
    if portal_type in allowed_types:
        return super(LeadImageViewlet, self).render()
    else:
        return ''

LeadImageViewlet.render = render


def bodyTag(self, css_class='newsImage'):
    """ returns img tag """
    context = aq_inner(self.context)
    field = context.getField(IMAGE_FIELD_NAME)
    if field is not None and \
            field.getFilename(context) is not None and \
            field.get_size(context) != 0:
        scale = self.prefs.body_scale_name
        try:
            return field.tag(context, scale=scale, css_class=css_class)
        except:
            return ''
    return ''

LeadImageViewlet.bodyTag = bodyTag


# security.declareProtected(permissions.View, 'tag')
def tag(self, instance, scale=None, height=None, width=None, alt=None,
        css_class=None, title=None, **kwargs):
    """Create a tag including scale
    """
    image = self.getScale(instance, scale=scale)
    if image:
        img_width, img_height = self.getSize(instance, scale=scale)
    else:
        img_height = 0
        img_width = 0

    if height is None:
        height = img_height
    if width is None:
        width = img_width

    url = instance.absolute_url()
    if scale:
        url += '/' + self.getScaleName(scale)
    else:
        url += '/' + self.getName()

    if alt is None:
        alt = instance.Title()
    if title is None:
        title = instance.Title()

    if isinstance(alt, str):
        alt = alt.decode('utf-8', 'replace')
    if isinstance(title, str):
        title = title.decode('utf-8', 'replace')

    values = {'src': url,
              'alt': escape(alt, quote=True),
              'title': escape(title, quote=True),
              'height': height,
              'width': width,
             }

    result = '<img src="%(src)s" alt="%(alt)s" title="%(title)s" '\
             'height="%(height)s" width="%(width)s"' % values

    if css_class is not None:
        result = '%s class="%s"' % (result, css_class)

    for key, value in kwargs.items():
        if value:
            result = '%s %s="%s"' % (result, key, value)

    return '%s />' % result

ImageField.tag = tag
