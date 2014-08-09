def doNothing(*args, **kwargs):
    pass

def decorator(before=doNothing,after=doNothing):
    def outer(func):
        def inner(*args, **kwargs):
            before(*args, **kwargs)
            ret = func(*args, **kwargs)
            after(*args, **kwargs)
            return ret
        return inner
    return outer

def giveArgs(func):
    def inner(*args, **kwargs):
        return func()
    return inner
