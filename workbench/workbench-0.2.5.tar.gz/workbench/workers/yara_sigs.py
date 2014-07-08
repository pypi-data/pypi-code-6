
''' Yara worker '''
import os
import yara
import pprint


class YaraSigs(object):
    ''' This worker check for matches against yara sigs. 
        Output keys: [matches:list of matches] '''
    dependencies = ['sample']

    def __init__(self):
        self.rules = self.get_yara_rules()

    def get_yara_rules(self):
        ''' Recursively traverse the yara/rules directory for rules '''

        # Try to find the yara rules directory relative to the worker
        my_dir = os.path.dirname(os.path.realpath(__file__))
        yara_rule_path = os.path.join(my_dir, 'yara/rules')
        if not os.path.exists(yara_rule_path):
            raise RuntimeError('yara could not find yara rules directory under: %s' % os.getcwd())

        # Okay load in all the rules under the yara rule path
        self.rules = yara.load_rules(rules_rootpath=yara_rule_path) 

        return self.rules

    def execute(self, input_data):
        ''' yara worker execute method '''
        raw_bytes = input_data['sample']['raw_bytes']
        matches = self.rules.match_data(raw_bytes)
        return {'matches': matches}


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' yara.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    workbench = zerorpc.Client()
    workbench.connect("tcp://127.0.0.1:4242")

    # Store all the files in directory and make an md5 list
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pe/bad')
    file_list = [os.path.join(data_dir, child) for child in os.listdir(data_dir)]
    md5_list = []
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as pe_file:
            md5_list.append(workbench.store_sample(filename, pe_file.read(), 'pe'))

    # Store the md5 list on the server as a sample set
    workbench.store_sample_set(md5_list)

    # Grab one of the sample for input to the local unit test
    input_data = workbench.get_sample(md5_list[0])

    # Execute the worker (unit test)
    worker = YaraSigs()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    pprint.pprint(output)

    # Execute the worker (server test)
    output = workbench.batch_work_request('yara_sigs', {'md5_list': md5_list})
    get_all_output = list(output)
    print '\n<<< Server Test >>>'
    pprint.pprint(get_all_output)

if __name__ == "__main__":
    test()
