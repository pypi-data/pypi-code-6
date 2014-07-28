"""This client pulls PCAP 'views' (view summarize what's in a sample)."""

import zerorpc
import os
import pprint
import client_helper
import flask

STATIC_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../data/')

APP = flask.Flask(__name__, template_folder=STATIC_DIR,
                  static_folder=STATIC_DIR, static_url_path='')

def run():
    """This client pulls PCAP 'views' (view summarize what's in a sample)."""
    
    # Grab grab_server_argsrver args
    args = client_helper.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    data_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '../data/pcap')
    file_list = [os.path.join(data_path, child) for child in \
                os.listdir(data_path)]
    results = []
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        # Process the pcap file
        with open(filename,'rb') as f:
            md5 = workbench.store_sample(filename, f.read(), 'pcap')
            results.append([filename.split('/')[-1], workbench.work_request('view_pcap', md5)])

    return results

@APP.route('/')
def flask_app():
    '''Return redered template for the flask app'''
    results = run()
    return flask.render_template('templates/index.html', results=results)            

def test():
    ''' pcap_bro_view test '''
    run()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True)

