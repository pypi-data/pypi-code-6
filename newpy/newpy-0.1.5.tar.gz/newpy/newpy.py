""" newpy, created by Edward """

import argparse
from os import makedirs
import os.path
import io

PROJECT_LOCATION = ""
PROJECT_NAME = ""
RESOURCES = "..resources/"
LOGGER = None

def generate_project_dir(force):
    print("generating project dir")
    try:
        makedirs(PROJECT_LOCATION, exist_ok=force)
    except PermissionError:
        return 1
    except FileExistsError:
        # this can't get raise if force is set
        return 2

def generate_gitignore():
    print("generating gitignore")
    with open(PROJECT_LOCATION + ".gitignore", "w") as f:
        f.write("*.pyc\n")
        f.write("__pycache__\n")

def generate_py(replacements):
    if LOGGER:
        skeleton_file = RESOURCES + "skeleton_with_logger.py"
        generate_logger(replacements)
    else:
        skeleton_file = RESOURCES + "simple_skeleton.py"

    with open(PROJECT_LOCATION + PROJECT_NAME + ".py", "w") as outfile:
        outfile.write(make_replacements(skeleton_file, replacements))

def generate_logger(replacements):
    """ TODO: The logger format is just a placeholder currently and needs
        improving. Must include name of file that made the log
    """
    logger_file = RESOURCES + "logger.py"
    with open(PROJECT_LOCATION + "Logger.py", "w") as outfile:
        outfile.write(make_replacements(logger_file, replacements))

def make_replacements(infile, replacements):
    with open(infile, "r") as f:
        buffer = io.StringIO(f.read())

    outfile = io.StringIO()
    for line in buffer:
        tmp_line = line
        for k, v in replacements.items():
            tmp_line = tmp_line.replace(k, v)
        outfile.write(tmp_line)

    return outfile.getvalue()

def main(args):
    global PROJECT_LOCATION
    global PROJECT_NAME
    global LOGGER
    PROJECT_LOCATION = os.path.normpath(args.project_location) + os.path.sep
    PROJECT_NAME=os.path.basename(os.path.normpath(PROJECT_LOCATION))
    LOGGER=args.logger

    result = generate_project_dir(args.force)
    if result is 1:
        print("Could not create project directory, please specify another location")
        return result
    elif result is 2:
        print("Could not create project directory, directory already exists")
        return result

    generate_gitignore()
    generate_py(args.replacements)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="newpy - for creating new python projects.")
    parser.add_argument("project_location", help="Please supply a directory for your new project. For example just `project_name` if you want it created in the current directory, or `/home/user/project_name` to create it in your home directory")
    parser.add_argument("-f", "--force", help="Force the creation of a new project, overwritting the directory if it exists already.", action="store_true")
    parser.add_argument("-d", "--description", help="Describe your new project", default="sample description")
    parser.add_argument("-a", "--author", help="What's your name?", default="")
    parser.add_argument("-l", "--logger", help="Do you want to create a logger?", action="store_true")
    args = parser.parse_args()

    args.replacements = {
            "$DESCRIPTION": args.description,
            "$AUTHOR": args.author,
            }

    exit(main(args))
else:
    print("example usage: python -m newpy")
