""" Pylint support. """

from __future__ import absolute_import

from os import path as op
import sys

from pylama.lint import Linter as BaseLinter # noqa

CURDIR = op.abspath(op.dirname(__file__))
sys.path.insert(0, CURDIR)

from radon.complexity import cc_visit_ast, ComplexityVisitor
from radon.metrics import mi_compute, h_visit_ast
from radon.raw import analyze


class Linter(BaseLinter):

    """ Check code with radon. """

    @staticmethod
    def run(path, code, complexity=10, maintability=30, **meta): # noqa
        """ Pylint code checking.

        :return list: List of errors.

        """
        import ast

        errors = []
        ast_node = ast.parse(code)

        # Check Complexity
        for result in cc_visit_ast(ast_node):
            if result.complexity >= complexity:
                errors.append(
                    dict(
                        type='C',
                        lnum=result.lineno,
                        text='C901 %r is too complex (%d)' % (
                            result.name, result.complexity)
                    )
                )

        # Check Maintainability
        raw = analyze(code)
        comments = (raw.comments + raw.multi / float(raw.sloc) * 100
                    if raw.sloc != 0 else 0)
        hv = h_visit_ast(ast_node)
        rank = mi_compute(
            hv.volume,
            ComplexityVisitor.from_ast(ast_node).total_complexity, raw.lloc,
            comments)
        if rank <= maintability:
            errors.append(dict(
                type="C", lnum=1,
                text="C999 The module has low maintainability index (%d)" % rank)) # noqa

        return errors
