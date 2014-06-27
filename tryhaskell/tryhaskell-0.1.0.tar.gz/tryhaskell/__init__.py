# -*- coding: utf-8 -*-

__version__ = '0.1.0'
__author__ = 'Cary Robbins <carymrobbins@gmail.com>'

from collections import namedtuple
import re
import sys
import requests


class TryHaskell:
    Result = namedtuple('Result', 'ok, expr, files, stdout, type, value')

    class Error(Exception):
        pass

    @classmethod
    def _bad_result(cls, error):
        """
        :param str error: Syntax error from TryHaskell.
        :rtype: TryHaskell.Result
        """
        return cls.Result(ok=False, expr='', files={}, stdout='', type='', value=error)

    @classmethod
    def eval(cls, exp):
        """
        :param str exp: Haskell expression to evaluate.
        :rtype: str
        """
        return cls.show(cls.get(exp))

    @classmethod
    def get(cls, exp):
        """
        :param str exp: Haskell expression to evaluate.
        :rtype: TryHaskell.Result
        """
        return cls.parse(cls.raw(exp))


    @classmethod
    def raw(cls, exp):
        """
        :param str exp: Haskell expression to evaluate.
        :rtype: dict
        """
        try:
            return requests.get('http://tryhaskell.org/eval', params={'exp': exp}).json()
        except ValueError as e:
            raise cls.Error(e)

    @classmethod
    def parse(cls, j):
        """
        :param dict j: JSON response from TryHaskell.
        :rtype: TryHaskell.Result
        """
        error = j.get('error')
        if error:
            return cls._bad_result(error)
        try:
            return cls.Result(ok=True, **j.get('success'))
        except ValueError as e:
            raise cls.Error(e)

    @classmethod
    def show(cls, result):
        """
        :param TryHaskell.Result result: Parse result of JSON data.
        :rtype: str
        """
        out = []
        if result.stdout:
            out.append('\n'.join(result.stdout))
        if not cls._is_function_value(result.value):
            out.append(result.value)
        return '\n'.join(out).strip() or ':: ' + result.type

    @classmethod
    def repl(cls):
        print('Press Ctrl+C to exit the repl.')
        try:
            while True:
                sys.stdout.write('> ')
                sys.stdout.flush()
                exp = sys.stdin.readline()
                # Trap Ctrl+D
                if not exp:
                    break
                exp = exp.strip()
                if exp in ['exit', 'quit']:
                    break
                elif exp.startswith(':t'):
                    exp = exp[2:].strip()
                    print(exp + ' :: ' + cls.get(exp).type)
                elif exp:
                    print(cls.eval(exp))
        except KeyboardInterrupt:
            pass
        print('Exiting repl.')

    @classmethod
    def _is_function_value(cls, value, regex=re.compile(r'^.*<.*->.*>.*$')):
        return regex.match(value)


if __name__ == '__main__':
    TryHaskell.repl()
