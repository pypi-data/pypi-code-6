__all__ = ['acl', 'hooks']

from functools import wraps

from _term import Hict, gen_uuid_bytes
from _exc import Unauthorized
import _config as conf

acl_rules = dict(role=lambda s, roles, *args, **argd: s.role in roles and role in s.profile.roles,  # noqa
                 user=lambda s, users, *args, **argd: s.profile.username in users,                  # noqa
                 origin=lambda s, origins, *args, **argd: s.origin in origins,
                 domain=lambda s, domains, *args, **argd: s.domain in domains)


def set_acl_rule(name, func):
    acl_rules[name] = func


def acl(**rules):

    for k, v in rules.iteritems():
        validator = acl_rules.get(k, v)
        assert callable(validator), ('invalid-acl', k)
        rules[k] = (v, validator)

    def decorator(f):

        from _state import get_state

        @wraps(f)
        def wrapper(*args, **argd):
            _state_ = get_state()
            for k, (v, validator) in rules.iteritems():
                try:
                    if v is validator:
                        valid = validator(_state_, *args, **argd)
                    else:
                        valid = validator(_state_, v, *args, **argd)
                except:
                    valid = False

                if valid is True:
                    continue
                elif valid is False:
                    raise Unauthorized(k)
                else:
                    raise Unauthorized(k, valid)

            return f(*args, **argd)

        return wrapper

    return decorator


def _undefined(name):

    def wrapper(*argv, **argd):
        raise NotImplementedError(name)

    return wrapper


def _default(key):
    key = key.upper()

    assert hasattr(conf, key), key

    def _default(*args, **argd):
        return getattr(conf, key)
    _default.is_default = True

    return _default

hooks = Hict(load_state=_undefined('hooks.load_state'),
             store_state=_undefined('hooks.store_state'),
             active_user_sessions=_undefined('hooks.active_user_sessions'),
             destroy_user_sessions=_undefined('hooks.destroy_user_sessions'),
             max_active_user_sessions=_default('max_active_user_sessions'),
             fetch_profile=_undefined('hooks.fetch_profile'),
             has_permission=_undefined('hooks.has_permission'),
             store_prelogin=_undefined('hooks.store_prelogin'),
             incr_abuse=_undefined('hooks.incr_abuse'),
             max_pads_count=_default('max_pads_count'),
             pad_grace_time=_default('pad_grace_time'),
             max_origin_abuse_level=_default('max_origin_abuse_level'),
             abuse_level_watch_period=_default('abuse_level_watch_period'),
             abuse_level_by_origin=_undefined('hooks.abuse_level_by_origin'),
             prelogin_grace_time=_default('prelogin_grace_time'),
             prelogin_count=_undefined('hooks.prelogin_count'),
             max_prelogin_count=_default('max_prelogin_count'),
             session_timeout=_default('session_timeout'),
             gen_session_id=gen_uuid_bytes)

default_settings = tuple(k for k, v in hooks.items()
                         if getattr(v, 'is_default', False))
