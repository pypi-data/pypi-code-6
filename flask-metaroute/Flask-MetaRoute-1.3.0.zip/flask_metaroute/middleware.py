from flask_metaroute.metaroute import MetaRoute


def MetaRouteMiddleware(app, package):
    return MetaRoute.Apply(app.__self__, package).wsgi_app


def MetaRouteMiddlewareAppFactory(app, global_config, package):
    return MetaRouteMiddleware(app, package)
