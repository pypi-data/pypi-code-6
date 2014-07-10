"""
This module makes routing, argument validation and dispatching of
Remote Procecure Calls on top of zeromq. This RPC is intended to be used
for internal in-site procedure call. If you want to open it for internet
you might need more security related tweaks here.
"""
import asyncio
import msgpack

from .core import Context, Scope, endpoint, resource


RPC = Scope('rpc')


class RPCRequest(object):

    deserializer = msgpack.load
    serializer = msgpack.dump

    def __init__(self, message):
        try:
            delim = message.index(b'')
            self.address = message[:delim]
            method, args, kwargs = self.deserializer(message[delim+1])
            method = method.decode('ascii')
            assert isinstance(args, list), "Args are bad"
            assert isinstance(kwargs, dict), "Kwargs are bad"
        except (ValueError, AssertionError, IndexError) as e:
            log.exception("Bad input %r", e)
        self.path =


class RPCServerProto(object):
    scope = RPC
    context_factory = Context
    request_factory = RPCRequest


    def __init__(self, *, resources=()):
        self.resources = resources

    @asyncio.coroutine
    def _resolve(self, request):
        ctx = self.context_factory
        for i in self.resources:
            ctx.start(i,
                *self.positional_arguments_factory(ctx),
                **self.keyword_arguments_factory(ctx))
            resolver = i.get_resolver_for_scope(self.site_scope)
            if resolver:
                try:
                    return (yield from resolver.resolve(ctx))
                except OutOfScopeError:
                    continue
        else:
            raise NotFound()
