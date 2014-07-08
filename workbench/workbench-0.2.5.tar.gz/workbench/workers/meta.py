
''' Meta worker '''
import hashlib
import magic
import pprint

class MetaData(object):
    ''' This worker computes meta data for any file type. '''
    dependencies = ['sample']

    def __init__(self):
        ''' Initialization '''
        self.meta = {}

    def execute(self, input_data):
        ''' This worker computes meta data for any file type. '''
        raw_bytes = input_data['sample']['raw_bytes']
        self.meta['md5'] = hashlib.md5(raw_bytes).hexdigest()
        self.meta['type_tag'] = input_data['sample']['type_tag']
        with magic.Magic() as mag:
            self.meta['file_type'] = mag.id_buffer(raw_bytes[:1024])
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as mag:
            self.meta['mime_type'] = mag.id_buffer(raw_bytes[:1024])
        with magic.Magic(flags=magic.MAGIC_MIME_ENCODING) as mag:
            self.meta['encoding'] = mag.id_buffer(raw_bytes[:1024])
        self.meta['file_size'] = len(raw_bytes)
        self.meta['filename'] = input_data['sample']['filename']
        self.meta['import_time'] = input_data['sample']['import_time']
        self.meta['customer'] = input_data['sample']['customer']
        self.meta['length'] = input_data['sample']['length']

        return self.meta


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' meta.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    workbench = zerorpc.Client()
    workbench.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    import os
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '../data/pe/bad/033d91aae8ad29ed9fbb858179271232')
    md5 = workbench.store_sample('bad_pe', open(data_path, 'rb').read(), 'pe')
    input_data = workbench.get_sample(md5)

    # Execute the worker (unit test)
    worker = MetaData()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    pprint.pprint(output)

    # Execute the worker (server test)
    output = workbench.work_request('meta', md5)
    print '\n<<< Server Test >>>'
    pprint.pprint(output)

if __name__ == "__main__":
    test()
