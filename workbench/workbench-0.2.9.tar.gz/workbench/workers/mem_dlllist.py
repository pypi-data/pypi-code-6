
''' Memory Image DllList worker. This worker utilizes the Rekall Memory Forensic Framework.
    See Google Github: http://github.com/google/rekall
    All credit for good stuff goes to them, all credit for bad stuff goes to us. :)
'''
import os
import hashlib
import mem_base

class MemoryImageDllList(mem_base.MemoryImageBase):
    ''' This worker computes dlllist for memory image files. '''
    dependencies = ['sample']

    def __init__(self):
        ''' Initialization '''
        super(MemoryImageDllList, self).__init__()
        self.set_plugin_name('dlllist')

    @staticmethod
    def safe_key(key):
        return key.replace('.','_')

    def execute(self, input_data):
        output = super(MemoryImageDllList, self).execute(input_data)

        # Organize the output a bit
        # This worker has 'keys' for each process and the value is a list of dlls
        # The 'Info' section has nothing for this worker so we're going to remove it.
        processes = output['sections'].keys()
        processes.remove('Info')

        # The 'safe_key' call is because Mongo can't have keys with a period in them so
        # when the data gets saved into Mongo the '.' will be replaced with a '_' so
        # doing that replacment now explicitly so it doesn't bite us later on.
        output['tables'] = [self.safe_key(process) for process in processes]
        for process in processes:
            output[self.safe_key(process)] = output['sections'][process]

        # No longer need the sections data
        del output['sections']

        return output

# Unit test: Create the class, the proper input and run the execute() method for a test
import pytest
@pytest.mark.rekall
def test():
    ''' mem_dlllist.py: Test '''

    # This worker test requires a local server running
    import zerorpc
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect("tcp://127.0.0.1:4242")

    # Store the sample
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/memory_images/exemplar4.vmem')
    with open(data_path, 'rb') as mem_file:
        raw_bytes = mem_file.read()
        md5 = hashlib.md5(raw_bytes).hexdigest()
        if not workbench.has_sample(md5):
            md5 = workbench.store_sample('exemplar4.vmem', open(data_path, 'rb').read(), 'mem')

    # Execute the worker (unit test)
    worker = MemoryImageDllList()
    output = worker.execute({'sample':{'raw_bytes':raw_bytes}})
    print '\n<<< Unit Test >>>'
    print 'dlllist(truncated): %s' % str(output)[:1000]
    assert 'Error' not in output

    # Execute the worker (server test)
    output = workbench.work_request('mem_dlllist', md5)
    print '\n<<< Server Test >>>'
    print 'dlllist(truncated): %s' % str(output)[:1000]
    assert 'Error' not in output


if __name__ == "__main__":
    test()
