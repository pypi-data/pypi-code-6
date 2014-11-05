from functools import wraps


__version__ = "0.1"


def get_version():
    return __version__


def next_version():
    _v = __version__.split('.')
    _v[-1] = str(int(_v[-1]) + 1)
    return '.'.join(_v)


def validate_request(validator):
    def _json_selector(obj, current_selector):
        json_dict = obj.get_json(force=True, silent=True) or {}
        return [(current_selector + ['json'], json_dict)]
    
    def decorator(func):
        from flask import current_app, request, g

        @wraps(func)
        def inner_func(*args, **kwargs):
            g.request_validation_result = \
                current_app.extensions['gladiator'].validate(
                    validator, request, ctx={
                        'custom_selectors': {
                            'json!': _json_selector
                        }
                    })
            if g.request_validation_result.success:
                return func(*args, **kwargs)
            else:
                return g.request_validation_result.errors
        return inner_func
    return decorator


class Gladiator(object):
    """This class is used to control the Gladiator integration to one
    or more Flask applications."""

    def __init__(self, app=None, default_validation_ctx=None):
        self.default_validation_ctx = default_validation_ctx
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def _default_ctx(self, ctx=None):
        ret = {}
        if self.app.config.get('GLADIATOR_VALIDATION_CTX', None):
            ret.update(self.app.config.get('GLADIATOR_VALIDATION_CTX'))
        if self.default_validation_ctx is not None:
            ret.update(self.default_validation_ctx)
        if ctx is not None:
            ret.update(ctx)
        return ret

    def init_app(self, app):
        app.config.setdefault('GLADIATOR_VALIDATION_CTX', None)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['gladiator'] = self

    def validate(self, validator, obj, selector=None, ctx=None, **kw):
        from gladiator.core import validate as _validate

        _ctx = self._default_ctx(ctx)
        result = _validate(validator, obj, selector, ctx=_ctx, **kw)
        return result
