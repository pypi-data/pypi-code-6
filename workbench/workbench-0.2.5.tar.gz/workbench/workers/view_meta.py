
''' view_meta worker '''
import pprint

class ViewMetaData(object):
    ''' ViewMetaData: Generates a view for meta data on the sample '''
    dependencies = ['meta']

    def execute(self, input_data):
        ''' Execute the ViewMetaData worker '''

        # Deprecation unless something more interesting happens with this class
        return input_data['meta']

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_meta.py: Unit test'''
    
    # This worker test requires a local server running
    import zerorpc
    workbench = zerorpc.Client()
    workbench.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    import os
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '../data/pe/bad/033d91aae8ad29ed9fbb858179271232')
    md5 = workbench.store_sample('bad_pe', open(data_path, 'rb').read(), 'pe')
    input_data = workbench.get_sample(md5)
    input_data.update(workbench.work_request('meta', md5))

    # Execute the worker (unit test)
    worker = ViewMetaData()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    pprint.pprint(output)

    # Execute the worker (server test)
    output = workbench.work_request('view_meta', md5)
    print '\n<<< Server Test >>>'
    pprint.pprint(output)

if __name__ == "__main__":
    test()
