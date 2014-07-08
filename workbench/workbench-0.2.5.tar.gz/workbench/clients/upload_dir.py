''' This client pushes a big directory of different files into Workbench '''
import zerorpc
import os
import workbench_client
import hashlib


def run():
    ''' This client pushes a big directory of different files into Workbench '''
    
    # Grab server args
    args = workbench_client.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+args['server']+':'+args['port'])
    
    # Grab all the filenames from the data directory
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pe/bad')
    file_list = [os.path.join(data_dir, child) for child in os.listdir(data_dir)]

    # Upload the files into workbench
    for path in file_list:
        with open(path,'rb') as f:
            filename = os.path.basename(path)

            # Here we're going to save network traffic by asking
            # Workbench if it already has this md5
            raw_bytes = f.read()
            md5 = hashlib.md5(raw_bytes).hexdigest()
            if workbench.has_sample(md5):
                print 'Workbench already has this sample %s' % md5
            else:
                # Store the sample into workbench
                md5 = workbench.store_sample(filename, raw_bytes, 'unknown')
                print 'Filename %s uploaded: type_tag %s, md5 %s' % (filename, 'unknown', md5)

import pytest
@pytest.mark.xfail
def test():
    ''' file_upload test '''
    run()

if __name__ == '__main__':
    run()

