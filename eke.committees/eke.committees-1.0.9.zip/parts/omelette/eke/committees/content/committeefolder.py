# encoding: utf-8
# Copyright 2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Committee folder.'''

from eke.knowledge.content import knowledgefolder
from eke.committees.config import PROJECTNAME
from eke.committees.interfaces import ICommitteeFolder
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements

CommitteeFolderSchema = knowledgefolder.KnowledgeFolderSchema.copy() + atapi.Schema((
    # No extra fields
))

finalizeATCTSchema(CommitteeFolderSchema, folderish=True, moveDiscussion=False)

class CommitteeFolder(knowledgefolder.KnowledgeFolder):
    '''Committee Folder which contains Committees.'''
    implements(ICommitteeFolder)
    portal_type = 'Committee Folder'
    schema      = CommitteeFolderSchema

atapi.registerType(CommitteeFolder, PROJECTNAME)
