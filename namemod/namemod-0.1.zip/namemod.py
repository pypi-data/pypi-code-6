'''
Created on 30/05/2014

@author: Ronaldo Webb
'''
import sys

import nm.args
import nm.processors as processor
import nm.exceptions as exceptions
import registry

if __name__ == '__main__':
    try:

        args = nm.args.AppArgs.getInstance()
        file_processor = processor.FileProcessor(args, registry)
        file_processor.process()
        
    except exceptions.TargetFolderNotFoundException as tfnfe:
        
        print("Error: {}".format(tfnfe))
        sys.exit(-1)

    except exceptions.FileAndFolderProcessingException as fafpe:
        
        print("Error: {}".format(fafpe))
        sys.exit(-1)
        
    except Exception as ex:
        
        raise
    
    else:
        
        print("Finished")
        
    sys.exit(0)