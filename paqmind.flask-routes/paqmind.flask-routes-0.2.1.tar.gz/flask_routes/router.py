class Router():
    def __init__(self, bp):
        self.bp = bp


    def route(self, cls):
        """Use as decorator for class methods (basic, not @classmethod or @static)"""
        # Bind routes to blueprint
        nameset = set()
        for subcls in cls.mro()[:-1]:
            for attrname, attrvalue in subcls.__dict__.items():
                is_callable = callable(attrvalue)
                is_public = not attrname.startswith('_')
                is_routable = hasattr(attrvalue, 'routable')
                if is_callable and is_public and is_routable:
                    if attrvalue.routable and attrname not in nameset:
                        def func(attrname=attrname, *args, **kwargs):
                            return getattr(cls(self.bp), attrname)(*args, **kwargs)
                        for route in getattr(cls, attrname).routes:
                            route = route.copy()
                            # Rule
                            mask = route['options'].pop('rulemask', None) or '/{view}/{rule}'
                            url = cls.endpoint if cls.url is None else cls.url
                            rule = mask.format(view=url.strip('/'), rule=route['rule'].lstrip('/'))
                            # Endpoint
                            mask = route.pop('endpoint', None) or '{view}:{func}'
                            endpoint = mask.format(view=cls.endpoint, func=attrname)
                            # Apply...
                            self.bp.add_url_rule(rule, endpoint, func, **route['options'])
                    nameset.add(attrname)
        cls.routable = True


def route(rule, endpoint=None, **options):
    def decorated(func):
        # Active case: route class method
        if hasattr(func, 'routable'):
            func.routes.append({
                'rule': rule,
                'endpoint': endpoint,
                'options': options,
            })
        else:
            func.routable = True
            func.routes = [{
                'rule': rule,
                'endpoint': endpoint,
                'options': options,
            }]
        return func
    return decorated


def unroute(func):
    setattr(func, 'routable', False)
    return func
