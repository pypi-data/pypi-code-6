def foo(x):
    if x < 0:
        return 0
    else:
        return bar(x) - 1


def bar(x):
    return baz(x) - 1


def baz(x):
    #print 'hi'
    return quux(x) - 1


def quux(x):
    return foo(x - 1) - 1


class MyClass(object):
    def foo(self, x):
        if x < 0:
            return 0
        else:
            return self.bar(x) - 1

    def bar(self, x):
        return self.baz(x) - 1

    def baz(self, x):
        #print 'hi'
        return self.quux(x) - 1

    def quux(self, x):
        return self.foo(x - 1) - 1


