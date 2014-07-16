from django import template

from webapp.models import Career

register = template.Library()

@register.inclusion_tag('webapp/get_careers.html')
def get_careers(user):
    careers = Career.objects.filter(user=user)
    return {'careers': careers}
