
''' Memory Image base worker. This worker utilizes the Rekall Memory Forensic Framework.
    See Google Github: https://github.com/google/rekall
    All credit for good stuff goes to them, all credit for bad stuff goes to us. :)
'''

import os
from rekall_adapter.rekall_adapter import RekallAdapter

class MemoryImageBase(object):
    ''' This worker computes meta-data for memory image files. '''
    dependencies = ['sample']

    def __init__(self):
        ''' Initialization '''
        self.output = {}
        self.plugin_name = 'imageinfo'

    def set_plugin_name(self, name):
        ''' Set the name of the plugin to be used '''
        self.plugin_name = name

    def execute(self, input_data):
        ''' Execute method '''

        # Grab the raw bytes of the sample
        raw_bytes = input_data['sample']['raw_bytes']

        # Spin up the rekall adapter
        adapter = RekallAdapter(raw_bytes)
        session = adapter.get_session()
        renderer = adapter.get_renderer()

        # Here we can grab any plugin
        try:
            plugin = session.plugins.__dict__[self.plugin_name]()
        except KeyError:
            print 'Could not load the %s Rekall Plugin.. Failing with Error.' % self.plugin_name
            return {'Error': 'Could not load the %s Rekall Plugin' % self.plugin_name}

        # Render the plugin and return the data
        self.output = renderer.render(plugin)
        return self.output


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' mem_base.py: Test '''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Do we have the memory forensics file?
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/memory_images/exemplar4.vmem')
    if not os.path.isfile(data_path):
        print 'Not finding exemplar4.mem... Downloading now...'
        import urllib
        urllib.urlretrieve('https://s3-us-west-2.amazonaws.com/workbench-data/memory_images/exemplar4.vmem', data_path)

    # Did we properly download the memory file?
    if not os.path.isfile(data_path):
        print 'Downloading failed, try it manually...'
        print 'wget https://s3-us-west-2.amazonaws.com/workbench-data/memory_images/exemplar4.vmem'
        exit(1)

    # Store the sample
    md5 = c.store_sample('exemplar4.vmem', open(data_path, 'rb').read(), 'mem')

    # Unit test stuff
    input_data = c.get_sample(md5)

    # Execute the worker (unit test)
    worker = MemoryImageBase()
    worker.set_plugin_name('imageinfo')
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # Execute the worker (server test)
    output = c.work_request('mem_base', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)


if __name__ == "__main__":
    test()
