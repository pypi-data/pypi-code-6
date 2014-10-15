from fuf import mainfunc, SelfInit

def test_falsemain():
    x = []
    @mainfunc
    def main():
        x.append(5)

    assert not x, "False main incorrectly called"

def test_main():
    x = []
    def main():
        x.append(5)
    main.__module__ = '__main__'
    main = mainfunc(main)

    assert x, "main not called"

def test_selfinit():
    @SelfInit
    class foo(object):
        def __init__(self):
            self.x = 'test'
        def __call__(self):
            return self.x
    assert foo() == 'test', "Self Initialization failed"

def test_selfinitconstructor():
    @SelfInit('test')
    class foo(object):
        def __init__(self, arg):
            self.x = arg
        def __call__(self):
            return self.x
    assert foo() == 'test', "Self Initialization with argument failed"
