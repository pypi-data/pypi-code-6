'''
Created on 30/05/2014

@author: Ronaldo Webb
'''
import argparse
import threading

import nm.exceptions as nm_exceptions

APP_VERSION = "0.1"
CREATED_BY = "M0bG3n"

class AppArgs(object):
    _APP_ARGS = None
    _lock = threading.RLock()
    
    def __init__(self, args):
        parser = argparse.ArgumentParser(prog="namemod"
            ,description="Simplifying multiple files or folders renames.")
        
        #Positional Arguments
        parser.add_argument("folder", help="Specifies the target folder to process.")
        parser.add_argument("old_name_segment", help="Old name segment to be renamed.")
        parser.add_argument("new_name_segment", help="New name segment.")
        
        #Optional Arguments
        parser.add_argument("-f", "--file-only", action="store_true", help="Process only files.")
        parser.add_argument("-F", "--folder-only", action="store_true", help="Process only folders.")
        parser.add_argument("-i", "--interactive", action="store_true", help="Ask confirmation before renaming.")
        parser.add_argument("-I", "--include-target-folder", action="store_true", help="Include the target folder in renaming.")
        parser.add_argument("-m", "--mode", choices=["text", "regex"], default="text", help="Default: %(default)s")
        parser.add_argument("-n", "--noop", action="store_true", help="Inhibit the actual renamig but display the intended outcome.")
        parser.add_argument("-R", "--recursive", help="Recursive", action="store_true")
        parser.add_argument("-xr", "--exclude-file-regex", metavar="regex", help="Exclude files by regex.")
        parser.add_argument("-xt", "--exclude-file-text", metavar="text", help="Exclude files by exact text match.")
        parser.add_argument("-Xr", "--exclude-folder-regex", metavar="regex", help="Exclude folders by regex.")
        parser.add_argument("-Xt", "--exclude-folder-text", metavar="text", help="Exclude folders by exact text match.")
        parser.add_argument("-v", "--version", action="version", version="%(prog)s {} - {}".format(APP_VERSION, CREATED_BY))

        #parser.add_argument("-o", "--output-folder", metavar="folder", help="Specify the destination folder of the processed files/folders.")
        #parser.add_argument("-r", "--rollback-enabled", metavar="identifier", help="Specify the identifier for rollback.")
   
        parser.parse_args(args, namespace=self)
        
        if (not self.file_only and not self.folder_only):
            self.file_only = True
        
        if self.file_only and self.folder_only:
            raise nm_exceptions.FileAndFolderProcessingException(nm_exceptions.FileAndFolderProcessingException.MESSAGE1)
    
    @staticmethod
    def getInstance(args=None, singleton=True):
        if singleton: 
        
            with AppArgs._lock:
                if (not AppArgs._APP_ARGS):
                    with AppArgs._lock:
                        if (not AppArgs._APP_ARGS):
                            AppArgs._APP_ARGS = AppArgs(args)
            return AppArgs._APP_ARGS
        
        else: 
        
            return AppArgs(args)