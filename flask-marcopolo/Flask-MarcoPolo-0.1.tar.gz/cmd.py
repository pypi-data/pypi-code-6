"""
Flask-MarcoPolo

Command line tool to create new project with MarcoPolo

Go in to the directory you want to create the project

flask-marcopolo -c [project_name]
"""

import os
import shutil
import argparse
from flask_marcopolo import __NAME__, __version__

CWD = os.getcwd()
TPL_PROJECT_DIR = os.path.dirname(__file__) + "/__project__"


def copy_recursive(src, dest, replace=False):
    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dest)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if replace and os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def get_project_dir_path(project_name):
    return "%s/%s" % (CWD, project_name)


def create_project(project_name, template="default"):

    project_dir = get_project_dir_path(project_name)
    _template = TPL_PROJECT_DIR + "/" + template
    run_tpl = TPL_PROJECT_DIR + ("/run_%s.py.tpl" % template)
    run_file = "%s/run_%s.py" % (CWD, project_name)

    if not os.path.isdir(project_dir):
        os.makedirs(project_dir)
    else:
        raise OSError("Project dir '%s' exists already " % project_name)

    with open(run_tpl, "r") as tpl:
        if not os.path.isfile(run_file):
            with open(run_file, "wb") as f:
                f.write(tpl.read().format(project_name=project_name))

    copy_recursive(_template, project_dir)


def main():
    """
    Main Application
    """
    print("-" * 80)
    print("%s %s" % (__NAME__, __version__))
    print("")

    parser = argparse.ArgumentParser()
    parser.add_argument("project_name",
                        help="Project name"
                        )
    parser.add_argument("-c", "--create",
                        help="To create a new project."
                             " [flask-marcopolo -c project_name]",
                        action="store_true")

    arg = parser.parse_args()

    try:
        if arg.project_name:
            project_name = arg.project_name
            if arg.create:
                create_project(project_name, "default")
                print("+ Project '%s' created" % project_name)
    except Exception as ex:
        print("- ERROR: %s" % ex.__str__())



