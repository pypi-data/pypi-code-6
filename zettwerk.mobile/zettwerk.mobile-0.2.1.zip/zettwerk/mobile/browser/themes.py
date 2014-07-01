import zipfile
import os.path

from zope.publisher.browser import BrowserView
from zope.component import getUtility

from plone.registry.interfaces import IRegistry
from plone.resource.interfaces import IResourceDirectory

from Products.statusmessages.interfaces import IStatusMessage

from zettwerk.mobile import contentMessageFactory as _


RESOURCE_NAME = 'zettwerkmobile'


class ConfiguredTheme(BrowserView):

    def __call__(self):
        registry = getUtility(IRegistry)
        return registry['zettwerk.mobile.interfaces.IThemesSettings' \
                        '.themename'] or 'default'


class ThemeUploadForm(BrowserView):

    def __call__(self):
        uploaded_theme_name = self.update_zip()
        if uploaded_theme_name:
            ## set the uploaded as active theme
            self._set_active_theme(uploaded_theme_name)

        elif self.request.get('active_theme'):
            self._set_active_theme(self.request.get('active_theme'))

        return self.index()

    @property
    def active_theme(self):
        registry = getUtility(IRegistry)
        return registry['zettwerk.mobile.interfaces.IThemesSettings.themename']

    @property
    def available_themes(self):
        persistentDirectory = getUtility(IResourceDirectory, name="persistent")
        if RESOURCE_NAME not in persistentDirectory:
            return []

        return persistentDirectory[RESOURCE_NAME].listDirectory()

    def _set_active_theme(self, name):
        """ """
        if type(name) is str:
            name = name.decode('utf-8')

        registry = getUtility(IRegistry)
        registry['zettwerk.mobile.interfaces.IThemesSettings.themename'] = name

    def _get_theme_name_of_zip(self, zip):
        """ we are searching a file, ending of .css in the
        first themes subfolder """

        for filename in zip.namelist():
            parts = os.path.split(filename)
            if len(parts) == 2 and parts[0] == 'themes':
                prefix = parts[1]
                splitted = prefix.split('.')
                if len(splitted) == 2 and splitted[1] == 'css':
                    return splitted[0]

    def update_zip(self):
        zip = self.request.get('zip', '')
        if not zip:
            return

        zip = zipfile.ZipFile(self.request.form.get('zip'))
        theme_name = self._get_theme_name_of_zip(zip)
        if not theme_name:
            IStatusMessage(self.request).add(_(u"Invalid Zipfile"),
                                             type="error")
            return

        persistentDirectory = getUtility(IResourceDirectory, name="persistent")
        if RESOURCE_NAME not in persistentDirectory:
            persistentDirectory.makeDirectory(RESOURCE_NAME)

        container = persistentDirectory[RESOURCE_NAME]

        ## force replace when a theme gets updated
        if theme_name in container:
            del container[theme_name]

        container.makeDirectory(theme_name)
        target = container[theme_name]
        target.importZip(zip)
        return theme_name
