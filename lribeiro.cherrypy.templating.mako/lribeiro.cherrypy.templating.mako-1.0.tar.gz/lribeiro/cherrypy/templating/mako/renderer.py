from .lookup import get_lookup


def mako_renderer(template_name, context):
    lookup = get_lookup()
    template = lookup.get_template(template_name)
    return template.render(**context)