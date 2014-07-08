''' This client pulls PCAP meta data '''
import zerorpc
import os
import pprint
import workbench_client

def run():
    ''' This client pulls PCAP meta data '''
    
    # Grab server args
    args = workbench_client.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    # Test out PCAP data
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pcap')
    file_list = [os.path.join(data_path, child) for child in os.listdir(data_path)]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as f:
            md5 = workbench.store_sample(filename, f.read(), 'pcap')
            results = workbench.work_request('view_pcap', md5)
            print 'Filename: %s results:' % (filename)
            pprint.pprint(results)

def test():
    ''' pcap_meta test '''
    run()

if __name__ == '__main__':
    run()

