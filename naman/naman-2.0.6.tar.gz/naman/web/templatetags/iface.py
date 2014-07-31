from django.template import Library


register = Library()


@register.inclusion_tag("forms/filters.html")
def filters(filtro, action="", name=None, ajax_container=None):
    if name == None:
        name = "fil"

    return {"action": action, "filtro": filtro, "name": name, "ajax_container": ajax_container}
