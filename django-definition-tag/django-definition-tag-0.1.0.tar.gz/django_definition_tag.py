from django.template import Node, TemplateSyntaxError


def definition_tag(register):
    """
    Decorator for template tag functions

    The "tag function" returns a value which, when called inside a template, is stored in a
    variable or displayed directly.

    Example:

    @definition_tag(register=register)
    def top_players(context):
        return TopScores.objects.order_by('-elo')[:20]

    Inside the template, we could call {% top_players %} to output the data, or we could call
    {% top_players as foo %} {{ foo }}.
    """
    def dec1(func):
        funcname = getattr(func, "_decorated_function", func).__name__
        def dec2(parser, token):
            tokens = token.split_contents()

            def raiseerror():
                raise TemplateSyntaxError(
                    "Call as '{% {0} %}' or '{% {0}  as varname %}'".format(funcname))
            if len(tokens) == 1:
                varname = None
            elif len(tokens) == 3:
                if tokens[1] != 'as':
                    raiseerror()
                varname = tokens[2]
            else:
                raiseerror()
            return DefineNode(func=func, name=varname)
        register.tag(funcname, dec2)
        return dec2
    return dec1


class DefineNode(Node):
    def __init__(self, name, func):
        self.func = func
        self.name = name

    def __repr__(self):
        return "<DefineNode>"

    def get_value(self, context):
        return self.func(context)

    def render(self, context):
        if self.name is None:
            return self.get_value(context)
        else:
            context[self.name] = self.get_value(context)
            return ''
