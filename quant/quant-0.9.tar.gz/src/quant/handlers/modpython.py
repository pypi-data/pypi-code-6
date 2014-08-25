import os, sys

def handler(req):
    os.environ.update(req.subprocess_env)
    try:
        import quant.soleInstance
        from django.core.handlers.modpython import ModPythonHandler
        class ModPythonHandler(ModPythonHandler):
            def __call__(self, req):
                return super(ModPythonHandler, self).__call__(req)
    except Exception, inst:
        msg = "sys.path: %s -- %s" % (sys.path, inst)
        raise Exception, msg
    return ModPythonHandler()(req)

