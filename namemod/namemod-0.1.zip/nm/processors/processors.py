'''
Created on 2/06/2014

@author: Ronaldo Webb
'''

import os
import os.path as path
import itertools
import re

import rx.subjects as rx_subject

import nm.exceptions as nm_exceptions

class FileProcessor(object):
    '''
    The main class for processing the file(s) or folder(s) for rename.
    '''
  
    @property
    def register(self):
        return self.__register

    def __init__(self, args, registry):
        self._args = args
        self._files = None
        self.__register = registry
        
    def __shouldInclude(self, folder, file = None): 
        '''
        The method that decides if the folder of file should be included in the process.
        
        Keyword arguments:
            folder -- the folder to be checked
            file -- optional file to be checked.
        '''

        search_in_file = ""
        (_, _, last_folder) = folder.rpartition(path.sep)

        if file:
            search_in_file = file
            
        if folder:
            if self._args.exclude_folder_regex:
                if re.search(self._args.exclude_folder_regex, last_folder):
                    return False
                
            if self._args.exclude_folder_text:
                if last_folder == self._args.exclude_folder_text:
                    return False
                
        if file:
            if self._args.exclude_file_regex:
                if re.search(self._args.exclude_file_regex, search_in_file):
                    return False

            if self._args.exclude_file_text:
                if self._args.exclude_file_text == search_in_file:
                    return False

        if "text" == self._args.mode and ((not file and last_folder == self._args.old_name_segment) or file == self._args.old_name_segment):
            return True
        
        if "regex" == self._args.mode and ((not file and re.search(self._args.old_name_segment, last_folder)) or re.search(self._args.old_name_segment, search_in_file)):
            return True

        return False
        
    def files(self, os_file):
        '''
        Returns the file(s) or folder(s) to be processed.
        
        Keyword Arguments:
            os_file -- the basis of files to be returned.
        '''
        
        item_files = []
        item_folders = []
        
        (dirpath, dirnames, filenames) = os_file
        
        if self._args.recursive:
            if self._args.file_only:
                item_files = (path.join(dirpath, file) for file in filenames
                    if self.__shouldInclude(dirpath, file))
    
            if self._args.folder_only:        
                if self.__shouldInclude(dirpath):
                    item_folders = [dirpath]
        else:
            if self._args.file_only:
                item_files = (path.join(dirpath, file) for file in filenames if self.__shouldInclude(dirpath, file))
            
            if self._args.folder_only:
                
                (_, _, last_folder) = dirpath.rpartition(path.sep) 

                if (((self._args.folder==dirpath and self._args.include_target_folder) or not dirnames) and 
                        (
                            (self._args.mode == "text" and last_folder == self._args.old_name_segment)
                               or
                            (self._args.mode == "regex" and re.search(self._args.old_name_segment, last_folder))
                        )
                        and self.__shouldInclude(dirpath)
                    ):
                    item_folders = [dirpath]
                else:
                    item_folders = (path.join(dirpath, dirname) for dirname in dirnames if self.__shouldInclude(dirname))
             
        self._files = itertools.chain(item_files, item_folders)
        
        return self._files
    
    def createEvent(self, file, *args, **kwargs): 
        '''
        Creator of the events to be used to the actions to be performed.
        
        Keyword Arguments:
            file -- the file or folder to be included in the event. 
        '''
        
        return self.register.createEvent(self, file)
    
    def runActions(self, file):
        '''
        The runner of the actions to be performed.
        
        Keyword Arguments:
            file -- the file or folder to run the action.
        '''
        
        action_event = self.createEvent(file)
        return_status = 0
        
        for (action, shouldExecute, forceReturn) in sorted(self.register.actions, key=lambda reg: reg[0].ACTION_ID):
            
            if shouldExecute(self):
                return_code = action.action(action_event)
                
                if return_code == self.register.interactive_no_response:
                    print("Skipping:", file)
                    return return_code
                elif return_code == self.register.ok_rename_status:
                    return return_code
                elif return_code:
                    raise nm_exceptions.ActionException("Error processing: {}".format(file))
                    break
                
                if forceReturn:
                    return return_status
                       
        return return_status

    def process_file(self): 
        '''
        The main method for processing files.
        '''
        
        subj_file = None
        subs_file = None
        
        if not (self._args.interactive or self._args.folder_only): 
            subj_file = rx_subject.Subject()

        if subj_file:
            subs_file = subj_file.subscribe(
                lambda os_file: self.process_os_file(os_file)
                ,lambda ex: print("Error: ", ex)
            )
            
        for _, file in enumerate(os.walk(self._args.folder)):
            
            if subj_file:
                #reactive reactive flow
                subj_file.on_next(file)
            else:
                #non-reactive flow
                self.process_os_file(file)
                
            if not self._args.recursive:
                break
            
        if subj_file:
            subj_file.on_completed()
        
        if subs_file:
            subs_file.dispose()
    
    def process_full_path(self, fullpath, *vargs, **kwargs):
        '''
        The helper method for processing the folder.
        
        Keyword Arguments:
            fullpath -- the full path of the folder to be processed.
        '''
        
        def append_to_process(fullpath):
            if processed.count(fullpath) == 0:
                processed.append(fullpath)  
        
        if (path.isdir(fullpath)):

            dir_struct = (fullpath, [], [])
            processed = []
            
            if "processed" in kwargs:
                processed = kwargs["processed"]
                
            if not processed.__contains__(fullpath):
                
                for file in self.files(dir_struct):
                    
                    status = self.runActions(file)
                    if status in self.register.ok_status:
                        
                        append_to_process(self._args.folder)
                        
                        if self._args.interactive and status == self.register.interactive_no_response:

                            #Interactive Mode.
                            self.register.prepareProcessedFolder(processed, self, fullpath)
                            self.process_folder(self._args.folder, *vargs, processed=processed)

                        elif path.exists(self._args.folder):
                            
                            #Target folder exists.
                            self.register.prepareProcessedFolder(processed, self, fullpath)
                            self.process_folder(self._args.folder, *vargs, processed=processed)

                        else:
                        
                            #Target folder doesn't exists.
                            new_name = self.register.rename(self)
                            self._args.folder = new_name
                            append_to_process(new_name)
                            self.process_folder(new_name, *vargs, processed=processed)

                        return
            
            if self._args.recursive or ("bypass_target" in vargs):
                self.process_folder(fullpath, *vargs, processed=processed)
    
    def process_folder(self, target, *vargs, **kwargs):
        '''
        The main method for processing a folder. 
        
        Keyword Arguments:
            target -- The folder to be processed. 
        '''
        
        (_, _, last_folder) = target.rpartition(path.sep)
        
        processed = []
        if "processed" in kwargs:
            processed = kwargs["processed"]
        
        if not processed.__contains__(target) and ((not ("bypass_target" in vargs) and self._args.include_target_folder and self._args.folder == target) and (
                (self._args.mode == "text" and last_folder == self._args.old_name_segment)
            or 
                (self._args.mode == "regex" and re.search(self._args.old_name_segment, last_folder))   
            )): 
            
            if self._args.noop or self._args.interactive:
                self.process_full_path(target, "bypass_target", *vargs, **kwargs)
            else:
                self.process_full_path(target, *vargs, **kwargs)
            
            return
        
        new_vargs = vargs
        if "bypass_target" in vargs:
            new_vargs = tuple([varg for varg in list(vargs) if not varg == "bypass_target"])

        subj_file = None
        subs_file = None
        
        if not self._args.interactive: 
            subj_file = rx_subject.Subject()

        if subj_file:
            subs_file = subj_file.subscribe(
                lambda fullpath : self.process_full_path(fullpath, new_vargs, **kwargs)
                ,lambda ex: print("Error: ", ex)
            )
        
        for dirname in os.listdir(target):
            fullpath = path.join(target, dirname)
            
            if subj_file:
                #reactive flow
                subj_file.on_next(fullpath)
            else:
                #non-reactive flow
                self.process_full_path(fullpath, new_vargs, processed = processed)
                    
        if subj_file:
            subj_file.on_completed()
        
        if subs_file:
            subs_file.dispose()

    def process(self):
        '''
        The main entry-point for processing both file(s) and folder(s). 
        '''
        if not path.exists(self._args.folder):
            raise nm_exceptions.TargetFolderNotFoundException(
                nm_exceptions.TargetFolderNotFoundException.MESSAGE1.format(self._args.folder))
        
        if self._args.file_only:
            self.process_file()
        elif self._args.folder_only:
            self.process_folder(self._args.folder)
        
    def process_os_file(self, os_file):
        '''
        Helper method for processing file.
        
        Keyword Arguments:
            os_file -- the file to be processed.
        '''
        for file in self.files(os_file):
            self.runActions(file)
                