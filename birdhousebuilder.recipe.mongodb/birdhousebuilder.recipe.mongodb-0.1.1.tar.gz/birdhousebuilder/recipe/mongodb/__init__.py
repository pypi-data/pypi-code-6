# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe mongodb"""

import os
from mako.template import Template

import zc.buildout
from birdhousebuilder.recipe import conda, supervisor

templ_config = Template(filename=os.path.join(os.path.dirname(__file__), "mongodb.conf"))

class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.anaconda_home = b_options.get('anaconda-home', conda.anaconda_home())
        self.conda_channels = b_options.get('conda-channels')

    def install(self):
        installed = []
        installed += list(self.install_mongodb())
        installed += list(self.install_config())
        installed += list(self.install_program())
        return installed

    def install_mongodb(self):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'mongodb'})

        conda.makedirs( os.path.join(self.anaconda_home, 'etc') )
        conda.makedirs( os.path.join(self.anaconda_home, 'var', 'lib', 'mongodb') )
        conda.makedirs( os.path.join(self.anaconda_home, 'var', 'log', 'mongodb') )
        
        return script.install()
        
    def install_config(self):
        """
        install mongodb config file
        """
        result = templ_config.render(
            prefix=self.anaconda_home,
            )

        output = os.path.join(self.anaconda_home, 'etc', 'mongodb.conf')
        conda.makedirs(os.path.dirname(output))
        
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_program(self):
        script = supervisor.Recipe(
            self.buildout,
            self.name,
            {'program': 'mongodb',
             'command': '%s/bin/mongod --config %s/etc/mongodb.conf' % (self.anaconda_home, self.anaconda_home),
             'priority': '10',
	     'autostart': 'true',
	     'autorestart': 'false',
             })
        return script.install()

    def update(self):
        return self.install()

def uninstall(name, options):
    pass

