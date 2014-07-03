'''
Created on 8/06/2014

@author: Ronaldo Webb
'''

class ActionException(Exception):
    '''
    The exception raised when there's an error while processing the Action.
    '''
    pass

class FileAndFolderProcessingException(Exception):
    '''
    The exception raised when both the -f and -F options are used.
    '''
    MESSAGE1 = "Cannot use -f and -F at the same time. Please choose one..."

class TargetFolderNotFoundException(Exception):
    '''
    The exception raised when the target folder is not found.
    '''
    MESSAGE1 = "The folder \"{}\" is missing."
        