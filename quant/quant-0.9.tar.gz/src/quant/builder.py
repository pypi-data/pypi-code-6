import dm.builder
from dm.ioc import *

class ApplicationBuilder(dm.builder.ApplicationBuilder):
    """
    Extends core builder by adding new application features, and by overriding
    core features with replacements for, or extensions of, core features.
    """

    #
    # Add features.
    
    def construct(self):
        super(ApplicationBuilder, self).construct()
        # todo: remove the UrlBuilderProject code
        #features.register('UrlBuilderProject', self.findUrlBuilderProject())

    def findUrlBuilderProject(self):
        import quant.url
        return quant.url.UrlBuilderProject()
 
    #
    # Replace features.

    def findSystemDictionary(self):
        import quant.dictionary
        return quant.dictionary.SystemDictionary()

    def findModelBuilder(self):
        import quant.dom.builder
        return quant.dom.builder.ModelBuilder()

    def findCommandSet(self):
        import quant.command
        return quant.command.__dict__

    def findFileSystem(self):
        import quant.filesystem
        return quant.filesystem.FileSystem()

    def findAccessController(self):
        import quant.accesscontrol
        return quant.accesscontrol.AccessController()

