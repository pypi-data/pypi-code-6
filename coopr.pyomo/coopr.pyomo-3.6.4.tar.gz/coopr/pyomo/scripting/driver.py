#import argparse
import coopr.misc.coopr_parser
from coopr.pyomo import TransformationFactory
import textwrap


def main_exec(options):
    import coopr.environ
    wrapper = textwrap.TextWrapper()
    wrapper.initial_indent = '      '
    wrapper.subsequent_indent = '      '
    print("")
    for xform in sorted(TransformationFactory.services()):
        print("  "+xform)
        print(wrapper.fill(TransformationFactory.doc(xform)))


#
# Add a subparser for the check command
#
coopr.misc.coopr_parser.add_subparser('transformations',
        func=main_exec, 
        help='List the available model transformations.',
        description='This coopr subcommand is used to list the available model transformations.'
        )
