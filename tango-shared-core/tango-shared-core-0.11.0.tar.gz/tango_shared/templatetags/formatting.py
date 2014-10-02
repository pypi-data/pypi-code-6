from django.template import Library

register = Library()


@register.filter
def replace(value, arg):
    """
    Replaces one string with another in a given string
    usage: {{ foo|replace:"aaa|xxx"}}
    """

    replacement = arg.split('|')
    try:
        return value.replace(replacement[0], replacement[1])
    except:
        return value


@register.filter
def fixbreaks(value):
    """
    fixes line breaks to make markdown happy.
    Be careful. It won't play nice with para breaks.
    """
    return value.replace('\n', '  \n')


@register.filter
def humanized_join(value):
    """
    Given a list of strings, format them with commas and spaces,
    but with 'and' at the end.

    >>> humanized_join(['apples', 'oranges', 'pears'])
    "apples, oranges, and pears"

    In a template, if mylist = ['apples', 'oranges', 'pears']
    then {{ mylist|humanized_join }}
    will output "apples, oranges, and pears"

    """
    # convert ensure numbers are strings to avoid errors
    value = [unicode(item) for item in value]

    if len(value) == 1:
        return value[0]
    if len(value) == 2:
        return "%s and %s" % (value[0], value[1])

    # join all but the last element
    all_but_last = ", ".join(value[:-1])
    return "%s and %s" % (all_but_last, value[-1])
