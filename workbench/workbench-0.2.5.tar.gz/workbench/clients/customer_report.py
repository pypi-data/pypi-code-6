''' This client generates customer reports on all the samples in workbench '''
import zerorpc
import pprint
import os
import workbench_client

def run():
    ''' This client generates customer reports on all the samples in workbench '''
    
    # Grab server args
    args = workbench_client.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    results = workbench.batch_work_request('view_customer', {})
    pprint.pprint(list(results))

def test():
    ''' customer_report test '''
    run()

if __name__ == '__main__':
    run()

