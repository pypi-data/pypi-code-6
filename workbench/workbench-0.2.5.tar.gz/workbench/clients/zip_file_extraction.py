''' This client shows workbench extacting files from a zip file '''
import zerorpc
import os
import pprint
import workbench_client

def run():
    ''' This client shows workbench extacting files from a zip file '''
    
    # Grab server args
    args = workbench_client.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    # Test out zip data
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/zip')
    file_list = [os.path.join(data_path, child) for child in os.listdir(data_path)]
    for filename in file_list:
        with open(filename,'rb') as f:
            md5 = workbench.store_sample(filename, f.read(), 'zip')
            results = workbench.work_request('view', md5)
            print 'Filename: %s ' % (filename)
            pprint.pprint(results)

            # The unzip worker gives you a list of md5s back
            # Run meta on all the unzipped files.
            results = workbench.work_request('unzip', md5)
            print '\n*** Filename: %s ***' % (filename)
            for child_md5 in results['unzip']['payload_md5s']:
                pprint.pprint(workbench.work_request('meta', child_md5))

import pytest
@pytest.mark.xfail
def test():
    ''' simple_workbench_client test '''
    run()

if __name__ == '__main__':
    run()

