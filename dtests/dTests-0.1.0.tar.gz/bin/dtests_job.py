#!/usr/bin/env python

import dTests.utils.my_socket
import socket
import json
import argparse
import os
import dTests.utils.utils
from dTests.utils.utils import compile_file, exec_file

config = ''

def create_parser():
    parser = argparse.ArgumentParser(description='Run testcases distributively')
    subparsers = parser.add_subparsers(dest="type")

    # create the parser for the "new" command
    parser_new = subparsers.add_parser('new', help='Create a new dTests project')
    parser_new.add_argument('name', help='Project name')
    parser_new.add_argument('lang', help='Project language', choices=['cpp', 'java'])

    # create the parser for the "run" command
    parser_run = subparsers.add_parser('run', help='Runs an existing dTests project')
    parser_run.add_argument('--splitter', '-s', nargs=1,help='The splitter program')
    parser_run.add_argument('--program', '-p', nargs=1,help='The program itslef')
    parser_run.add_argument('--input', '-i', nargs=1,help='The program input')
    parser_run.add_argument('--config', '-c', nargs=1, default='config.json',help='The configuration json')
    return parser

def read_configuration(configuration_file):
    global config
    if not os.path.isfile(configuration_file):
        print "Error : Missing configuration file"
        exit()
    with open(configuration_file, 'r') as config_file:
        config = config_file.read()
    config = json.loads(config)

def run_project(args):
    read_configuration(args.config)
    lang = config["lang"]
    input_file = os.path.abspath(args.input or "input.in")
    program_file = os.path.abspath(args.program or "program."+lang)
    splitter_file = os.path.abspath(args.splitter or "splitter."+lang)
    
    if not os.path.isfile(input_file):
        print "Error : %s file is missing" % input_file
        exit()
    if not os.path.isfile(program_file):
        print "Error : %s file is missing" % program_file
        exit()
    if not os.path.isfile(splitter_file):
        print "Error : %s file is missing" % splitter_file
        exit()
    
    if not compile_file(program_file, lang):
        print "Error : %s file contains compilation errors" % program_file
        exit()

    if not compile_file(splitter_file, lang):
        print "Error : %s file contains compiltation errors" % splitter_file
        exit()

    _testcases = exec_file(splitter_file, lang).split(config["split_string"])
    if not _testcases[-1]: _testcases = _testcases[0:-1]
    test_counter = 0
    testcases = []
    for i in _testcases:
        testcases.append( [test_counter, i] )
        test_counter += 1
    job = {}
    job["source_file"] = program_file
    job["testcases"] = testcases
    job["lang"] = config["lang"]

    s = dTests.utils.my_socket.MySocket()
    s.connect(socket.gethostname(), 9001)
    s.send(json.dumps(job))
    print s.recv(),

def build_config_file(args):
    config = {}
    config["lang"] = args.lang
    config["split_string"] = "--split--\n"
    return json.dumps(config)

def new_project(args):
    lang = args.lang
    name = args.name
    os.mkdir(name)
    os.chdir(name)
    
    # Write config file
    config_file = build_config_file(args)
    f = file("config.json","w")
    f.write(config_file)
    f.close()

    # Write other files
    open("splitter."+lang, 'a').close()
    open("input.in", 'a').close()
    open("program."+lang, 'a').close()

if __name__ == '__main__':

    parser = create_parser() 
    args = parser.parse_args()
    if args.type == "run":
        run_project(args)
    elif args.type == "new":
        new_project(args)
