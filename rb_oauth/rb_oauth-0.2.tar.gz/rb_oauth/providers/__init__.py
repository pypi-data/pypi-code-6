from rb_oauth import _registry


REGISTRY = _registry.Registry()


def register(cls, name=None):
    if name is None:
        name = cls.INFO().button
    REGISTRY.register(cls, name)
    cls.add_settings()
    return cls


def extract_provider(args, callback=None):
    # XXX authid should be pulled from local storage (cookie?) rather
    # than pulled from args.
    authid = args.get('authid')
    try:
        provider = args['provider']
    except KeyError:
        raise RuntimeError('missing provider')
    try:
        cls = REGISTRY[provider]
    except KeyError:
        raise NotImplementedError('unknown OAuth provider: {!r}'
                                  .format(provider))
    next = args['next']
    return cls(authid, callback, next)
