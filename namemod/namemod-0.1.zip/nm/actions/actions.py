'''
Created on 30/05/2014

@author: Ronaldo Webb
'''

import abc
import re
import threading
import os
import os.path as os_path

class AbstractAction(metaclass=abc.ABCMeta): 
    '''
    The base class of all the Actions available 
    '''
    
    @abc.abstractmethod
    def action(self, action_event=None):
        '''
        The action that must be implemented by the subclass.
        
        Keyword arguments:
            action_event -- an instance of nm.actions.ActionEvent
        '''
        pass
     
class NOOPAction(AbstractAction):
    '''
    The action that doesn't commit anything but just displays what it is suppose to do.
    '''
    
    ACTION_ID = 200
    
    def action(self, action_event):
        data = action_event.data()
        args = data.get("args")
        file = data.get("file")
        collector = data.get("collector", None)
        new_name = RenameAction.new_name(file, args.old_name_segment, args.new_name_segment)
        prefix = "FILE"
        
        if not data.get("isfile"):
            prefix = "FOLDER"
            
        message = "[{}]\tRename {} -> {}".format(prefix, file, new_name)
        
        if type(collector) is list:
            collector.append(message)
            
        print(message)
        
        return 0
        
class InteractiveAction(AbstractAction):
    '''
    The action that ask for confirmation for every rename to be done.
    '''
    
    ACTION_ID = 100
    RESPONSE_YES = ACTION_ID - ACTION_ID
    RESPONSE_NO = ACTION_ID + 1
    
    _lock = threading.RLock()

    def action(self, action_event):
        data = action_event.data()
        args = data.get("args")
        file = data.get("file")
        collector = data.get("collector", None)
        
        interactive_index = data.get("interactive_index", 0)

        interactive_response = data.get("interactive_response", None)
        
        new_name = RenameAction.new_name(file, args.old_name_segment, args.new_name_segment)
 
        question = "Are you sure you want to rename {} to {}? [Y/n]".format(file, new_name)
        
        if type(collector) is list:
            collector.append(question)
        
        if interactive_response:
            print(question)
            if len(interactive_response) > 1 :
                response = interactive_response[interactive_index]
            else:
                response = interactive_response
        else:
            with(InteractiveAction._lock):
                response = input(question)
        
        if response.upper() == "N" or len(response.strip()) == 0:
            return InteractiveAction.RESPONSE_NO
            
        return InteractiveAction.RESPONSE_YES

class RenameAction(AbstractAction):
    '''
    The action that actually rename the file or folder.
    '''
    
    ACTION_ID = 300
    
    def action(self, action_event):
        data = action_event.data()
        args = data.get("args")
        old_name = data.get("file")
        new_name = RenameAction.new_name(old_name, args.old_name_segment, args.new_name_segment, args.mode)
        no_rename = data.get("no_rename", False)
        
        print("Renaming {} to {}".format(old_name, new_name))
        
        if no_rename:
            print("[NO_RENAME]")
        else:
            if os_path.exists(old_name):
                os.rename(old_name, new_name)
                print("Renamed")
                return RenameAction.ACTION_ID
            else:
                print("{} doesn't exists".format(old_name))
            
        return 0
    
    @staticmethod
    def new_name(orig_name, old_name_segment, new_name_segment, mode="text", *args, **kwargs):
        
        def _regex_rename(orig, old_name, new_name):
            return re.sub(old_name, new_name, orig)
        
        def _text_rename(orig, old_name, new_name):
            return orig.replace(old_name, new_name)
        
        (head, tail) = os_path.split(orig_name)
        dict_mode = {
            "text": _text_rename,
            "regex": _regex_rename
        }
        
        new_tail = dict_mode[mode](tail, old_name_segment, new_name_segment)
        
        return os_path.join(head, new_tail)
