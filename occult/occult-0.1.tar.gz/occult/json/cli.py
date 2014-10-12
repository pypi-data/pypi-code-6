# -*- coding: utf-8 -*-

import os
import json
import codecs

import jsonschema


from ..libraries.minify_json import json_minify
from cliff.command import Command

from clint.textui import colored, puts, puts_err


class JSONUtility(Command):
    def get_parser(self, prog_name):
        parser = super(JSONUtility, self).get_parser(prog_name)
        subparsers = parser.add_subparsers()

        validate_parser = subparsers.add_parser('validate')
        validate_parser.add_argument('command', nargs='?', default='validate')
        validate_parser.add_argument('-i', '--instance', type = str, help = 'the json instance')
        validate_parser.add_argument('-s', '--schema', type=str, help = 'the json schema')

        syntax_parser = subparsers.add_parser('syntaxcheck')
        syntax_parser.add_argument('command', nargs='?', default='syntaxcheck')
        syntax_parser.add_argument('-s', '--schema', type=str, help = 'the json schema')

        return parser

    def take_action(self, parsed_args):
        command = parsed_args.command

        if command == 'validate':
            return self.validate(parsed_args)
        elif command == 'syntaxcheck':
            return self.syntaxcheck(parsed_args)

    def validate(self, parsed_args):
        instance_path = parsed_args.instance
        schema_path = parsed_args.schema

        schema_file = codecs.open(schema_path, 'rb', encoding='utf-8')
        instance_file = codecs.open(instance_path, 'rb', encoding='utf-8')

        schema_json = json.loads(json_minify(schema_file.read()), encoding='utf-8')
        instance_json = json.loads(json_minify(instance_file.read()), encoding='utf-8')

        schema_file.close()
        instance_file.close()

        validator = jsonschema.Draft4Validator(schema_json)
        errors = validator.iter_errors(instance_json)

        if validator.is_valid(instance_json):
            puts(colored.green('No Error Found.'))
            return

        for error in errors:
            puts('%s %s' % (colored.red('[' + str.upper(str(error.schema_path[0]) + ']')), error.message))

    def syntaxcheck(self, parsed_args):
        schema_path = parsed_args.schema
        schema_file = codecs.open(schema_path, 'rb', encoding='utf-8')
        schema_json = json.loads(json_minify(schema_file.read()), encoding='utf-8')
        schema_file.close()

        try:
            jsonschema.Draft4Validator.check_schema(schema_json)
            puts(colored.green('No Error Found.'))
        except Exception as e:
            puts(colored.red(e.message))


