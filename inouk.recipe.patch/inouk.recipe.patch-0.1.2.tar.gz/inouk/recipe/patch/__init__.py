# -*- coding: utf-8 -*-
"""Inouk Recipe patch"""

import logging
from subprocess import Popen, PIPE, STDOUT

import zc.buildout
_logger = logging.getLogger('inouk.recipe.patch')

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.binarypatch = options.get('binary-patch') or 'patch'

    def install(self):
        """Installer"""
        self.apply_patch()
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    def apply_patch(self):
        """
        patch -d basedirectory -N -i patch.patch
        patch --directory basedirectory --forward -input patch.patch
        """
        returncode = self.run_patch_command()
        if not (returncode is None or returncode == 0):
            raise zc.buildout.UserError('could not apply %s' % self.options['patch'])

    def reverse_patch(self):
        returncode = self.run_patch_command(revert=True)
        if not (returncode is None or returncode == 0):
            raise zc.buildout.UserError('could not revert patch %s' % self.options['patch'])

    def run_patch_command(self, revert=False):
        if revert:
            cmd = '--reverse'
        else:
            cmd = '--forward'

        patchfiles = self.options['patch']
        patchfiles = filter(None, patchfiles.split('\n'))  # split on each line filtering empty ones
        patchfiles = filter(None, [e.split('#')[0].strip() for e in patchfiles])  # build a list of patches by removing comment and filtering empty items

        for patchfile in patchfiles:
            patchcommand =[self.binarypatch,
                            '-p0',
                            cmd,
                            '--reject-file', '-', # Don't create reject file
                            '--directory', self.options['patchlocation'],
                            '--input', patchfile,
                       ]
            _logger.debug(' '.join(patchcommand))
            patcher = Popen(patchcommand,
                         stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            [_logger.debug(line.replace('\n','')) for line in patcher.stdout.readlines()]

            if not (patcher.returncode is None or patcher.returncode == 0):
                _logger.error('Error applying/reverting file %s' % patchfile)
                return patcher.returncode

        return 0

    def update(self):
        """
        Update behaviour depends on update_mode option:
        - apply
        - reverse_then_apply
        - do_nothing (default for unrecognized option)
        """
        _logger.debug("update()")
        self.update_mode = self.options.get('update_mode', None) 
        if self.update_mode not in ( 'apply', 'reverse_then_apply'):
            self.update_mode = None
        _logger.debug("  update_mode = %s" % self.update_mode)

        if self.update_mode:
            if self.update_mode=='reverse_then_apply':
                self.reverse_patch()
            self.apply_patch()


def uninstall_recipe(name, options):
    """ Try to reverse patch on uninstall """
    recipe = Recipe(None, name, options)
    recipe.reverse_patch()
