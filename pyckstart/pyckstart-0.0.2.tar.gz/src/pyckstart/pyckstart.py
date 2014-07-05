#!/usr/bin/python2
# -*- coding: utf-8 -*-

import shutil
import os
import sys

from jinja2 import Environment, PackageLoader, FileSystemLoader
import sh
import shutil
import optparse

import logging


class TemplateLoader(object):
    """ Shortcut to jinja2 templates accessor"""
    def __init__(self, root_path, logger):
        self.logger = logger
        self.logger.debug( "Initializing loader with path %s", root_path)
        self.loader = FileSystemLoader(root_path)
        self.env = Environment(loader=self.loader)

    def get_template(self, tpl_name):
        """ Shortcut to env.get_template"""
        return self.env.get_template(tpl_name)

class TemplatesLoader(object):
    """  Shortcut to handle systemwide/local templates """
    def __init__(self, root_path, local_path, logger):
        self.logger = logger
        # systemwide templates loader
        self.root_loader = TemplateLoader(root_path, logger)
        # local template loader
        self.local_loader = TemplateLoader(local_path, logger)

    def get_template(self, tpl_name):
        """ Shortcut to env.get_template, with systemwide/local location"""
        try:
            return self.local_loader.get_template(tpl_name)
        except:
            self.logger.debug("Could not load templates from local installation")
            return self.root_loader.get_template(tpl_name)

class Pyckstart(object):
    """ Pyckstart easy python module layout creator"""
    def __init__(self, options):
        self.options = options
        self.init_logger()
        self.init_paths()
        self.init_templates_loader()
        # TODO : support folder location to be passed as an argument


    def init_logger(self):
        if self.options.debug :
            logging.basicConfig(level = logging.DEBUG)
        elif not self.options.quiet:
            logging.basicConfig(level = logging.INFO)
        self.logger = logging.getLogger(__name__)

    def init_paths(self):
        # package destination location
        self.pkg_dest_folder = os.path.join(self.options.package_name)
        # get systemwide templates location
        module_path = os.path.dirname(os.path.realpath(__file__))
        self.root_files_path = os.path.join(module_path, 'files')
        # get local templates location
        home_dir = os.path.expanduser("~")
        self.local_files_path = os.path.join(home_dir, ".pyckstart", "files")

    def init_templates_loader(self):
        # initialize templates loader
        self.loader = TemplatesLoader(self.root_files_path, self.local_files_path, self.logger)

    def write_file(self, filename, content=''):
        """ Creates a new file and initializes it with the given content."""
        with open(filename, 'wb') as f:
            f.write(content)

    def create_folders(self, folders):
        """ Create module folders """
        for folder in folders:
            self.create_folder(folder)

    def create_folder(self, folder):
        self.logger.debug("Creating folder %s", folder)
        if not os.path.exists(folder):
            os.makedirs(folder)


    def write_template(self, copy_to, templates, values = {}):
        for tpl in templates:
            tpl_fullname = tpl+".tpl"
            if type(templates) == dict:
                outfile = templates[tpl]
            else:
                outfile = tpl
            self.logger.debug("Copying %s to %s", tpl_fullname, outfile)
            template = self.loader.get_template(tpl_fullname).render(values).encode('utf-8')
            self.write_file(os.path.join(copy_to, outfile), template)

    def create_basic_layout(self):
        """Create base module layout """
        if self.pkg_dest_folder is None :
            raise Exception("Package destination folder was None")
        # BASIC LAYOUT
        # could have beeen done with only one instruction
        # the directory creation is equivalent to mkdir -p
        self.logger.info("Creating basic layout")

        self.basic_layout_folders = [self.pkg_dest_folder,
                os.path.join(self.pkg_dest_folder, "src"),
                os.path.join(self.pkg_dest_folder, "src", self.options.package_name.lower()),
                ]

        # root files
        self.basic_layout_templates= [ "README.rst", "MANIFEST.in", "LICENCE.txt", "setup.py"]
        # Create layout
        self.create_folders(self.basic_layout_folders)
        self.write_template(self.pkg_dest_folder, self.basic_layout_templates, {"options" : self.options})

        src_path = os.path.join(self.pkg_dest_folder, "src", self.options.package_name.lower())
        self.write_template( src_path, ["__init__.py"], {"options" : self.options})
        self.write_template( src_path, { "package_name.py" : self.options.package_name.lower()+".py"}, {"options" : self.options})

    def create_cli_layout(self):
        self.logger.info("Creating CLI layout")
        """ Create module layout for command line entrypoint """
        cli_folder = os.path.join(self.pkg_dest_folder, "src", "bin")
        self.create_folder(cli_folder)
        self.write_template( cli_folder, { "bin/main.py" : self.options.package_name.lower()+".py"}, {"options" : self.options})
        self.write_template( cli_folder, { "bin/__init__.py" : "__init__.py"}, {"options" : self.options})

    def create_tests_layout(self):
        """ Create module layout for unitests """
        self.logger.info("Creating tests layout")
        cli_folder = os.path.join(self.pkg_dest_folder, "src", "tests")
        self.create_folder(cli_folder)
        self.write_template( cli_folder, { "tests/__init__.py" : "__init__.py"}, {"options" : self.options})
        self.write_template( cli_folder, { "tests/test_package_name.py" : "test_"+self.options.package_name.lower()+".py"}, {"options" : self.options})

    def create_git_layout(self):
        """ Create module layout for GIT and initialize the repo """
        self.logger.info("Creating git repository")
        module_folder = self.pkg_dest_folder

        git_folder = os.path.join(module_folder, ".git")

        self.write_template( module_folder, { "git/gitignore" : ".gitignore"}, {"options" : self.options})
        git = sh.git

        self.logger.info("Git init")
        git.init(_cwd=module_folder)

        # get an repo object
        repo = git.bake(_cwd=module_folder)
        # add the module folder to git
        self.logger.info("Adding files")
        repo.add(".")
        # commit
        self.logger.info("Initial commit")
        try:
            repo.commit(m='Initial commit')
        except (Exception) as e:
            self.logger.error(e.message)

    def install_templates(self):
        """ Install templates in user home folder"""
        if os.path.exists(self.local_files_path) and not self.options.force:
            self.logger.warn("%s already exists. use -f to overwrite.", self.local_files_path)
        else:
            self.logger.info("Installing templates to %s.", self.local_files_path)
            if os.path.exists(self.local_files_path):
                shutil.rmtree(self.local_files_path)
            shutil.copytree(self.root_files_path, self.local_files_path)
            self.logger.info("Done")


    def create_module(self):
        """ Create differents module layouts """
        if os.path.exists(self.pkg_dest_folder) and not self.options.force:
            self.logger.warn("%s already exists. use -f to overwrite.", self.pkg_dest_folder)
        else:
            self.create_basic_layout()
            if self.options.with_cli:
                self.create_cli_layout()
            if self.options.with_tests:
                self.create_tests_layout()
            if self.options.with_git:
                self.create_git_layout()


def main():
    parser = optparse.OptionParser("usage: %prog -n module_name [options]")

    parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Enable debug output")
    parser.add_option("-q", "--quiet", dest="quiet", action="store_true", default=False, help="Disable output")

    parser.add_option("-v", "--version", dest="version", action="store", type= "string", default="0.0.0.0", help="Module version")
    parser.add_option("-t", "--tests", dest="with_tests", action="store_true", default=False, help="Create tests layout")
    parser.add_option("-g", "--git", dest="with_git", action="store_true", default=False, help="Enable git repo creation")
    parser.add_option("-c", "--cli", dest="with_cli", action="store_true", default=False, help="Create CLI layout")

    parser.add_option("-p", "--pyversion", dest="py_version", action="store", default=sys.version_info.major, help="Python version for #!/usr/bin/env python#. Default value : current python major version (%s)" % sys.version_info.major)
    parser.add_option("-n", "--name", dest="package_name", action="store", default=None, help="Package name")

    parser.add_option("-i", "--install", dest="install", action="store_true", default=False, help="Install templates in home folder")
    parser.add_option("-f", "--force", dest="force", action="store_true", default=False, help="Will override existing files. Use with care.")

    (options, args) = parser.parse_args()

    p = Pyckstart(options)
    if options.install == True:
        p.install_templates()
    else:
        if options.package_name is None :
            parser.error("You must provide a package name. See --help")
        p.create_module()


if __name__ == "__main__":
    main()
