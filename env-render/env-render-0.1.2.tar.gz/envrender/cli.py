import os
import sys
import jinja2
import argparse
from .process import process_env

DESCRIPTION = 'Renders a template using the environment'

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('src_template', help='The template path')
parser.add_argument('output', help='The output path')
parser.add_argument('-d', '--docker', help='Process env vars for docker',
                    default=False, action="store_true")
parser.add_argument('-p', '--add-type-to-process', action='append',
                    dest='type_names_to_process',
                    help='Add a type prefix to process for the template')


def run(args=None):
    args = args or sys.argv[1:]

    parsed_args = parser.parse_args(args)

    type_names_to_process = parsed_args.type_names_to_process or []

    src_template_path = parsed_args.src_template

    output_path = parsed_args.output

    render(type_names_to_process, src_template_path, output_path, parsed_args.docker)


def render(type_names_to_process, src_template_path, output_path,
           process_docker=False):
    if not os.path.exists(src_template_path):
        raise Exception(
            'Source template "%s" could not be found' % src_template_path
        )

    context = process_env(type_names_to_process, os.environ,
                          process_docker=process_docker)

    src_template_str = open(src_template_path).read()

    rendered = jinja2.Template(src_template_str).render(**context)

    output_file = open(output_path, 'w')
    output_file.write(rendered)
    output_file.close()

if __name__ == '__main__':
    run()
