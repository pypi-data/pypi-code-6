
''' view worker '''
import zerorpc

class View(object):
    ''' View: Generates a view for any file type '''
    dependencies = ['meta']

    def __init__(self):
        self.workbench = zerorpc.Client()
        self.workbench.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):

        # Grab the mime_type from the input and switch view types
        md5 = input_data['meta']['md5']
        mime_type = input_data['meta']['mime_type']
        if mime_type == 'application/x-dosexec':
            result = self.workbench.work_request('view_pe', md5)
        elif mime_type == 'application/pdf':
            result = self.workbench.work_request('view_pdf', md5)
        elif mime_type == 'application/zip':
            result = self.workbench.work_request('view_zip', md5)
        elif mime_type == 'application/vnd.tcpdump.pcap':
            result = self.workbench.work_request('view_pcap', md5)
        elif mime_type == 'application/x-shockwave-flash':
            result = self.workbench.work_request('swf_meta', md5)
        else:
            # In the case of an unsupported MIME type just return the meta data
            result = input_data

        return result

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.workbench.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view.py: Unit test'''
    import pprint

    # This worker test requires a local server running
    workbench = zerorpc.Client()
    workbench.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    import os
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '../data/pdf/bad/067b3929f096768e864f6a04f04d4e54')
    md5 = workbench.store_sample('bad_067b39', open(data_path, 'rb').read(), 'pdf')
    input_data = workbench.work_request('meta', md5)

    # Execute the worker
    worker = View()
    output = worker.execute(input_data)
    print '\nView: '
    pprint.pprint(output)

    # Generate the input data for this worker
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '../data/pe/bad/033d91aae8ad29ed9fbb858179271232')
    md5 = workbench.store_sample('bad_033d91', open(data_path, 'rb').read(), 'pe')
    input_data = workbench.work_request('meta', md5)

    # Execute the worker
    output = worker.execute(input_data)
    print '\nView: '
    pprint.pprint(output)

    # Generate the input data for this worker
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '../data/zip/good.zip')
    md5 = workbench.store_sample('good.zip', open(data_path, 'rb').read(), 'zip')
    input_data = workbench.work_request('meta', md5)

    # Execute the worker
    output = worker.execute(input_data)
    print '\nView: '
    pprint.pprint(output)

if __name__ == "__main__":
    test()
