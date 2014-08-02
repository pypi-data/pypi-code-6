"""This client generates customer reports on all the samples in workbench."""

import zerorpc
import os
import client_helper

def run():
    """This client generates customer reports on all the samples in workbench."""
    
    # Grab server args
    args = client_helper.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    results = workbench.batch_work_request('view_customer')
    for customer in results:
        print customer['customer']

def test():
    """Executes test for customer_report."""
    run()

if __name__ == '__main__':
    run()

