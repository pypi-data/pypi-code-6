import pkg_resources
import shutil
import os
import argparse
import glob
import subprocess
import re
import platform


def patch_distutils_cfg():
    if platform.system() == 'Darwin':
        if not os.path.exists(os.path.expanduser("~/.pydistutils.cfg")):
            print "WARNING: Homebrew python on OS X has a goofy bug where distribute/pip fails to install things with prefixes. I can fix this by creating a ~/.pydistutils.cfg file for you. You can always delete this after running."
            if raw_input("Do you want me to create ~/.pydistutils.cfg for you? (y/N): ") in ('Y', 'y', 'yes', 'cool'):
                with open(os.path.expanduser("~/.pydistutils.cfg"), 'w') as f:
                    f.write('[install]\nprefix=')
            else:
                raise ValueError("Can not continue :/")


def read_requirements(reqfile):
    with open(reqfile, 'r') as file:
        data = file.read()
        requirements = list(pkg_resources.parse_requirements(data))
    return requirements


def clean_destination(target):
    if not os.path.exists(target):
        os.mkdir(target)
    files = glob.glob(os.path.join(target, "*"))
    for file in files:
        shutil.rmtree(file, True)


def clean_eggs(target):
    files = glob.glob(os.path.join(target, "*.egg-info"))
    for file in files:
        shutil.rmtree(file, True)
    files = glob.glob(os.path.join(target, "*.dist-info"))
    for file in files:
        shutil.rmtree(file, True)


def pip_install(target, package, pre):
    if pre:
        subprocess.check_call(["pip", "install", "--pre", "--target", target, package])
    else:
        subprocess.check_call(["pip", "install", "--target", target, package])


def install_packages(packages, destination, pre):
    """
    Installs all of the listed packages
    """
    for pkg in packages:
        pip_install(destination, str(pkg), pre)


def install_hook(destination):
    rx = re.compile(r'\# --- START GAELIC IMPORTER ---(.+)\# --- END GAELIC IMPORTER ---\n', re.DOTALL)
    output = ''
    if os.path.exists('appengine_config.py'):
        with open('appengine_config.py') as f:
            output = f.read()

    output = rx.sub('', output)

    hook = """
# --- START GAELIC IMPORTER ---

def gaelic_fix_path(path):
    import sys, os
    base = os.path.dirname(__file__)
    lib = os.path.join(base, path)
    if not lib in sys.path:
        sys.path.append(lib)


gaelic_fix_path('%s')

# --- END GAELIC IMPORTER ---\n
""" % (destination)

    output = hook + output.strip()

    with open('appengine_config.py', 'w') as f:
        f.write(output)


def main():
    parser = argparse.ArgumentParser(description='Gaelic (App Engine Link) installs packages for App Engine projects.')
    parser.add_argument('-r', '--requirements', help="pip requirements file", default="requirements.txt")
    parser.add_argument('-t', '--target', help="Directory to install packages (./lib)", default="lib")
    parser.add_argument('--pre', help="allow pre-release versions", action='store_true')
    args = parser.parse_args()

    patch_distutils_cfg()
    clean_destination(args.target)
    requirements = read_requirements(args.requirements)
    install_packages(requirements, args.target, args.pre)
    print 'Cleaning eggs'
    clean_eggs(args.target)
    print 'Installing importer hook'
    install_hook(args.target)
    print 'Done!'


if __name__ == "__main__":
    main()
