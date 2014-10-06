'''
Created on 20 oct. 2012

@author: coissac
'''

from distutils.command.build import build as ori_build


class build(ori_build):
    
    def has_ctools(self):
        return self.distribution.has_ctools()

    def has_files(self):
        return self.distribution.has_files()

    def has_executables(self):
        return self.distribution.has_executables()
    
    def has_ext_modules(self):
        return self.distribution.has_ext_modules()
    
    def has_littlebigman(self):
        return True
    
    sub_commands = [('littlebigman', has_littlebigman),
                    ('build_ctools', has_ctools),
                    ('build_files', has_files),
                    ('build_cexe', has_executables),
                    ('build_ext', has_ext_modules)] \
                   + ori_build.sub_commands
    
