
''' Memory Image ProcDump worker. This worker utilizes the Rekall Memory Forensic Framework.
    See Google Github: https://github.com/google/rekall
    All credit for good stuff goes to them, all credit for bad stuff goes to us. :)
'''

from rekall_adapter.rekall_adapter import RekallAdapter
import zerorpc
import contextlib
import tempfile
import shutil
import glob, os

class MemoryImageProcDump(object):
    ''' This worker dumps process pe files from memory image files. '''
    dependencies = ['sample']

    def __init__(self):
        ''' Initialization '''
        self.output = {}
        self.plugin_name = 'procdump'
        self.orig_dir = os.getcwd()

        # Spin up workbench connection
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")        

    def execute(self, input_data):
        ''' Execute method '''

        # Grab the raw bytes of the sample
        raw_bytes = input_data['sample']['raw_bytes']

        # Spin up the rekall adapter
        adapter = RekallAdapter(raw_bytes)
        session = adapter.get_session()
        renderer = adapter.get_renderer()

        # Create a temporary directory
        with self.make_temp_directory() as temp_dir:
            os.chdir(temp_dir)

            # Here we can grab any plugin
            try:
                plugin = session.plugins.procdump(dump_dir=temp_dir)
            except KeyError:
                print 'Could not load the %s Rekall Plugin.. Failing with Error.' % self.plugin_name
                return {'Error': 'Could not load the %s Rekall Plugin' % self.plugin_name}

            # Render the plugin and grab all the dumped files
            renderer.render(plugin)

            # Scrape any extracted files
            print 'mem_procdump: Scraping dumped files...'
            self.output['dumped_files'] = []
            for output_file in glob.glob('*'):

                # Store the output into workbench, put md5s in the 'dumped_files' field
                output_name = os.path.basename(output_file)
                output_name = output_name.replace('executable.', '')
                with open(output_file, 'rb') as dumped_file:
                    raw_bytes = dumped_file.read()
                    self.output['dumped_files'].append({'name': output_name, 
                                'md5':self.c.store_sample(output_name, raw_bytes, 'pe')})

        return self.output

    @contextlib.contextmanager
    def make_temp_directory(self):
        temp_dir = tempfile.mkdtemp()
        try:
            yield temp_dir
        finally:
            # Remove the directory/files
            shutil.rmtree(temp_dir)
            # Change back to original directory
            os.chdir(self.orig_dir)            

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()




# Unit test: Create the class, the proper input and run the execute() method for a test
import pytest
@pytest.mark.xfail
def test():
    ''' mem_procdump.py: Test '''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Store the sample
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/memory_images/exemplar4.vmem')
    md5 = c.store_sample('exemplar4.vmem', open(data_path, 'rb').read(), 'mem')

    # Unit test stuff
    input_data = c.get_sample(md5)

    # Execute the worker (unit test)
    worker = MemoryImageProcDump()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # Execute the worker (server test)
    output = c.work_request('mem_procdump', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)


if __name__ == "__main__":
    test()
