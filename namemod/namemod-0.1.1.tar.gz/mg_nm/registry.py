'''
Created on 1/07/2014

@author: Ronaldo Webb
'''

import os.path as path
import sys

import mg_nm.actions as nm_actions

#Default action available
actions = [
         #(action, shouldExecute, forceReturn, ok_status)
         (nm_actions.InteractiveAction(), lambda _self : _self._args.interactive, False),
         (nm_actions.NOOPAction(), lambda _self : _self._args.noop, True),
         (nm_actions.RenameAction(), lambda _self : True, False)
]

#Status used in FileProcessor.runActions() method.
ok_status = (nm_actions.RenameAction.ACTION_ID, nm_actions.InteractiveAction.RESPONSE_NO)

#No response status
interactive_no_response = nm_actions.InteractiveAction.RESPONSE_NO

ok_rename_status = nm_actions.RenameAction.ACTION_ID

def rename(processor):
    '''
    Default renamer method.
    
    Keyword Arguments:
        processor -- Instance of processor.
    '''
    return nm_actions.RenameAction.new_name(processor._args.folder
        , processor._args.old_name_segment
        , processor._args.new_name_segment
        , processor._args.mode)

def createEvent(processor, file, *args, **kwargs): 
    '''
    Creator of the events to be used to the actions to be performed.
    
    Keyword Arguments:
        processor -- Instance of FileProcessor
        file -- the file or folder to be included in the event. 
    '''
    
    return nm_actions.ActionEvent(
        args=processor._args
        ,file=file
        ,isfile=path.isfile(file)
        ,stream_out=sys.stdin
    )

def prepareProcessedFolder(processed, processor, fullpath):
    '''
    Used for recording processed fullpath.
    
    Keyword Arguments:
        processed -- List that constains already processed fullpath.
        processor -- Instance of processor.
        fullpath -- The fullpath to be added to the processed list.
    '''
 
    new_name = fullpath   
    if not path.exists(fullpath):
        new_name = nm_actions.RenameAction.new_name(fullpath, processor._args.old_name_segment, processor._args.new_name_segment, processor._args.mode)
    
    if processed.count(new_name) == 0:
        processed.append(new_name)
        
    return