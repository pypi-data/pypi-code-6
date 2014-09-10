# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.app.content.browser.foldercontents import (FolderContentsTable
                                                      , FolderContentsBrowserView
                                                      , FolderContentsView)


class PrenotazioniFolderContentsTable(FolderContentsTable):
    """
    The foldercontents table WITH NO BUTTONS
    """
    @property
    def buttons(self):
        ''' Custom buttons
        '''
        roles = api.user.get_roles()
        if 'Manager' in roles:
            return
        return []


class PrenotazioniFolderContentsView(FolderContentsView):
    '''
    The foldercontents CUSTOMIZED
    '''
    def contents_table(self):
        ''' Custom contetn-folder
        '''
        table = PrenotazioniFolderContentsTable(aq_inner(self.context),
                                                self.request)
        return table.render()


class PrenotazioniFolderContentsBrowserView(FolderContentsBrowserView):
    table = PrenotazioniFolderContentsTable
