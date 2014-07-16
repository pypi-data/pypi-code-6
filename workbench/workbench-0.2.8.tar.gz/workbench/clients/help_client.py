''' This client calls a bunch of help commands from workbench '''
import zerorpc
import pprint
import os
import workbench_client

def run():
    ''' This client calls a bunch of help commands from workbench '''
    
    # Grab server args
    args = workbench_client.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    # Call help methods
    print workbench.help()
    print workbench.help_basic()
    print workbench.help_commands()
    print workbench.help_command('store_sample')
    print workbench.help_workers()
    print workbench.help_worker('meta')
    print workbench.help_advanced()
    print workbench.list_all_workers()
    print workbench.test_worker('meta')
    

def test():
    ''' help_client test '''
    run()

if __name__ == '__main__':
    run()

