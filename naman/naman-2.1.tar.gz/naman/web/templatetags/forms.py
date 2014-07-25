from django.template import Library
from urlparse import urlparse, parse_qsl
from urllib import urlencode


register = Library()


@register.inclusion_tag("forms/filters.html")
def filters(filtro, action="", name=None, ajax_container=None):
    if name == None:
        name = "fil"

    return {"action": action, "filtro": filtro, "name": name, "ajax_container": ajax_container}


@register.inclusion_tag("forms/label.html")
def label(field, contents=None, attrs=None):
    if isinstance(attrs, basestring):
        attrs = [tuple(pair.split('=')) for pair in attrs.split(',')]
    attrs = dict(attrs or {})
    widget = field.field.widget
    for_id = widget.id_for_label(widget.attrs.get('id') or field.auto_id)
    contents = contents or field.label
    return {'field': field, 'id': for_id, 'contents': contents, 'attrs': attrs}


@register.inclusion_tag("forms/bootstrap_field.html")
def bootstrap_field(field, form_group_class=None, label_class=None, inner_div_class=None, input_field_class=None):
    widget = field.field.widget
    for_id = widget.id_for_label(widget.attrs.get('id') or field.auto_id)
    if input_field_class is not None:
        field.field.widget.attrs["class"] = input_field_class
    return {
        'field': field,
        'for_id': for_id,
        "form_group_class": form_group_class,
        "label_class": label_class,
        "inner_div_class": inner_div_class,
        }


@register.filter
def or_none(value):
    if value == None:
        return "-"
    return value


@register.filter
def attrlist(attrs):
    attrs = dict(attrs)

    ret = ""
    for k, v in attrs.items():
        ret += "%s=%s" % (k, v)
    return ret
attrlist.is_safe = True


@register.inclusion_tag("forms/pagination.html")
def paginator(paginator, objeto=None, urll=None):
    print "LA url es: %s" % urll
    return {
        "paginator": paginator,
        "objeto": objeto if objeto not in (None, "") else "P&aacute;gina",
        "urll": urll if urll != None else "",
        }


@register.inclusion_tag("forms/url_add_query_element.html")
def url_add_query_element(url, key, value):
    """
    appends a query element to an existing url
    """
    u = urlparse(url)
    data = dict(parse_qsl(u.query))

    data[key] = value

    return {"url": "%s?%s" % (u.path, urlencode(data))}


@register.inclusion_tag("forms/pagination_load.html")
def paginator_load(paginator, container, objeto=None, url=None):

    return {
        "paginator": paginator,
        "objeto": objeto if objeto != None else "P&aacute;gina",
        "url": url if url != None else "",
        "container": container,
        }


@register.filter('field_type')
def field_type(ob):
    return ob.field.widget.__class__.__name__
