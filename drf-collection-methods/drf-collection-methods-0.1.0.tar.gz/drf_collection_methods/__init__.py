from rest_framework.routers import replace_methodname, Route


class CollectionMethodRouterMixin(object):
    collection_route = Route(
        url=r'^{prefix}/{methodname}{trailing_slash}$',
        mapping={
            '{httpmethod}': '{methodname}',
        },
        name='{basename}-{methodnamehyphen}',
        initkwargs={}
    )

    def get_routes(self, viewset):
        ret = []

        dynamic_routes = []
        for methodname in dir(viewset):
            attr = getattr(viewset, methodname)
            httpmethods = getattr(attr, 'bind_to_collection_methods', None)
            if httpmethods:
                httpmethods = [method.lower() for method in httpmethods]
                dynamic_routes.append((httpmethods, methodname))

        route = self.collection_route
        for httpmethods, methodname in dynamic_routes:
            initkwargs = route.initkwargs.copy()
            initkwargs.update(getattr(viewset, methodname).kwargs)
            ret.append(Route(
                url=replace_methodname(route.url, methodname),
                mapping=dict((httpmethod, methodname) for httpmethod in httpmethods),
                name=replace_methodname(route.name, methodname),
                initkwargs=initkwargs,
            ))

        ret.extend(super(CollectionMethodRouterMixin, self).get_routes(viewset))
        return ret

def collection_link(**kwargs):
    def decorator(func):
        func.bind_to_collection_methods = ['get']
        func.kwargs = kwargs
        return func
    return decorator


def collection_action(methods=['post'], **kwargs):
    def decorator(func):
        func.bind_to_collection_methods = methods
        func.kwargs = kwargs
        return func
    return decorator
