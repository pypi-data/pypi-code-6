from wrapper import get, run
import logging
import requests


@get('/')
def f(*args, **kwargs):
    return '<html><head></head><body><h1>Hello!</h1></body></html>'

@get('/test', ['php'])
def test_f(*args, **kwargs):
    arguments = kwargs['arguments']
    php = arguments['php'][0]

    self = args[0]
    self.write("Head")

    return 'Test{}'.format(php)

def test():
    run(8888)

def main():
    pass


if __name__ == '__main__':
    test()