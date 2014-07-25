import os
import sys
import yaml
import argparse
import textwrap
import string
import time
import shutil
import distutils.core

from watchdog.observers import Observer
from handler import DeployEventHandler
from subprocess import Popen, call

def main():
    parser = argparse.ArgumentParser(
        prog="gaed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Google App Engine Deployer is a tool for deploying to various AppEngine projects to simulate environments
            (eg. Staging, Production, etc).

            This tool requires a basic YAML file for configuration which stores the paths and application names to use
            for the various environments. GAED allows an arbitrary number of environments to be supplied so should be
            flexible for any environment.

            Currently the following commands and subcommands are available:

            COMMAND     SUBCOMMAND              DESCRIPTION
            ------------------------------------------------------------------------------------------------------------
            config      init                    Initialises the current directory with the default YAML file that can be
                                                modified to suit.

                        generate                Generates the environment based off the YAML file.

            build       <environment>           Builds the specified environment as defined in the YAML file.

            serve       <environment>           Serves the specified environment locally so the site can be previewed.

            push        <environment>           Pushes the specified environment up to Google App Engine.

            watch                               Watch is used for local development and runs any frontend build tools as
                                                specified in the YAML file whenever a change occurs to a file in the
                                                development folder for the project.
            '''),
    )

    parser.add_argument('command', help='Main commands, GAE Deploy must always have one command')
    parser.add_argument('subcommand', help='Optional subcommand that should only follow certain commands as per above', nargs="?")

    args = parser.parse_args()


    # Lets see if we have a config file to work with, if it doesnt exist we'll die and inform the user
    # that they need a yaml config file
    try:
        with open('gaedeploy.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            valid_config = True
    except IOError:
        if args.command != "config" or args.subcommand != "init":
            print textwrap.dedent('''
                No config file present.
                Please run `gaed config init` to create the default yaml file.
                ''')
            exit(0)
        else:
            valid_config = False

    # Big Ugly Mappings of Commands/Subcommands to doing stuff
    # There must be a better way of doing this in Python
    if args.command == "config":
        if args.subcommand == "init":
            if not valid_config:
                import template
                with open('gaedeploy.yaml', 'w') as f:
                    f.write(template.config_yaml)
                print "Config Init!"
            else:
                print "ABORTING!!! You already have a configuration file!"
        elif args.subcommand == "generate":
            print "Config Generate!"
        elif args.subcommand == "check":
            print "Config Check!"
        else:
            print "Invalid subcommand"

    elif args.command == "build":
        print "Build %s" % args.subcommand

    elif args.command == "serve":
        print "Serve %s" % args.subcommand

    elif args.command == "push":
        print "Push %s" % args.subcommand

    elif args.command == "watch":
        # Lets grab the details of our dev environment from our config file
        for env, settings in config['environments'].iteritems():
            if env == "development":
                source_path = settings['path']
                watch_path = settings['watch']

        # We need to define a "preview" environment for our frontend tools to compile into for local development
        path = os.getcwd()

        source_directory = os.path.join(path, source_path)
        preview_directory = os.path.join(path, '.preview')
        watch_directory = os.path.join(path, watch_path)

        # Trash the existing preview directory
        if os.path.exists(preview_directory):
            shutil.rmtree(preview_directory)

        # Check if the folder exists, if it doesnt we want to create it
        if not os.path.exists(preview_directory):
            os.makedirs(preview_directory)

        # Next up we want to do a full file copy from our app folder to our preview folder
        # This is so that we dont have to watch the whole freaking wordpress folder!!!
        distutils.dir_util.copy_tree(source_directory, preview_directory)

        # From here on in we're working in our preview folder!
        os.chdir(preview_directory)
        if not os.path.isfile('app.yaml'):
            # No app.yaml means we cant start appengine, better throw an error and exit!
            print "We seem to be missing an app.yaml file. How are we supposed to start the dev server without it?"
            print "I thought you were better than that?!?"
            sys.exit(1)

        # Fire up AppEngine dev server asynchronously
        p = Popen(['/usr/local/bin/dev_appserver.py', '.'])

        # Run our build tools straight away
        event_handler = DeployEventHandler(path, config['tools']['build']['command'])

        # Start our observer to run our build script whenever our source changes
        observer = Observer()
        observer.schedule(event_handler, watch_directory, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            p.terminate()
        observer.join()
    else:
        print "Invalid command"

    sys.exit(0)

if __name__ == "__main__":
    main()
