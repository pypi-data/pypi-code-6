
''' Workbench: Open Source Security Framework '''

from gevent import monkey; monkey.patch_all(thread=False) # Monkey!
from gevent import signal as gevent_signal
import signal
import os
import zerorpc
import zmq
import logging
logging.basicConfig()
import StringIO
import json
import hashlib
import inspect
import funcsigs
import ConfigParser

# Workbench server imports
from . import data_store
from . import els_indexer
from . import neo_db
from . import plugin_manager
from bro import bro_log_reader


class WorkBench(object):
    ''' Workbench: Open Source Security Framework '''
    def __init__(self, store_args=None, els_hosts=None, neo_uri=None):

        # Open DataStore
        self.data_store = data_store.DataStore(**store_args)

        # ELS Indexer
        try:
            self.indexer = els_indexer.ELSIndexer(**{'hosts': els_hosts} if els_hosts else {})
        except SystemExit:
            print 'Could not connect to ELS. Is it running?'
            self.indexer = els_indexer.ELSStubIndexer(**{'uri': neo_uri} if neo_uri else {})

        # Neo4j DB
        try:
            self.neo_db = neo_db.NeoDB(**{'uri': neo_uri} if neo_uri else {})
        except RuntimeError:
            print 'Could not connect to Neo4j DB. Is it running?  $ neo4j start'
            self.neo_db = neo_db.NeoDBStub(**{'uri': neo_uri} if neo_uri else {})

        # Create Plugin Manager
        self.plugin_meta = {}
        plugin_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../workers')
        self.plugin_manager = plugin_manager.PluginManager(self._new_plugin, plugin_dir=plugin_dir)

    #
    # Sample Methods
    #
    def store_sample(self, filename, input_bytes, type_tag):
        ''' Store a sample into the DataStore.
            Args:
                filename: name of the file (used purely as meta data not for lookup)
                input_bytes: the actual bytes of the sample e.g. f.read()
                type_tag: ('pe','pcap','pdf','json','swf', or ...)
            Returns:
                the md5 of the sample
        '''
        return self.data_store.store_sample(filename, input_bytes, type_tag)

    def get_sample(self, md5):
        ''' Get a sample from the DataStore.
            Args:
                md5: the md5 of the sample
            Returns:
                A dictionary of meta data about the sample which includes
                a ['raw_bytes'] key that contains the raw bytes.
        '''
        sample = self.data_store.get_sample(md5)
        return {'sample': sample}

    def get_sample_window(self, type_tag, size):
        ''' Get a sample from the DataStore.
            Args:
                type_tag: the type of samples ('pcap','pe','pdf')
                size: the size of the window in MegaBytes (10 = 10MB)
            Returns:
                A list of md5s representing the newest samples within the size window
        '''
        return self.data_store.get_sample_window(type_tag, size)

    def has_sample(self, md5):
        ''' Do we have this sample in the DataStore.
            Args:
                md5: the md5 of the sample
            Returns:
                True or False
        '''
        return self.data_store.has_sample(md5)

    @zerorpc.stream
    def stream_sample(self, md5, max_rows):
        ''' Stream the sample by giving back a generator, typically used on 'logs'.
            Args:
                md5: the md5 of the sample
                max_rows: the maximum number of rows to return (None for all)
            Returns:
                A generator that yields rows of the file/log
        '''

        # Grab the sample and it's raw bytes
        sample = self.data_store.get_sample(md5)
        raw_bytes = sample['raw_bytes']

        # Figure out the type of file to be streamed
        type_tag = sample['type_tag']
        if type_tag == 'bro':
            bro_log = bro_log_reader.BroLogReader(convert_datetimes=False)
            mem_file = StringIO.StringIO(raw_bytes)
            generator = bro_log.read_log(mem_file)
            return generator
        elif type_tag == 'els_query':
            els_log = json.loads(raw_bytes)
            # Try to determine a couple of different types of ELS query results
            if 'fields' in els_log['hits']['hits'][0]:
                generator = (row['fields'] for row in els_log['hits']['hits'][:max_rows])
            else:
                generator = (row['_source'] for row in els_log['hits']['hits'][:max_rows])
            return generator
        elif type_tag == 'log':
            generator = ({'row':row} for row in raw_bytes.split('\n')[:max_rows])
            return generator
        elif type_tag == 'json':
            generator = (row for row in json.loads(raw_bytes)[:max_rows])
            return generator
        else:
            raise RuntimeError('Cannot stream file %s with type_tag:%s' % (md5, type_tag))

    #
    # Index Methods
    #
    def index_sample(self, md5, index_name):
        ''' Index a stored sample with the Indexer.
            Args:
                md5: the md5 of the sample
                index_name: the name of the index
            Returns:
                Nothing
        '''
        generator = self.stream_sample(md5, None)
        for row in generator:
            self.indexer.index_data(row, index_name)

    def index_worker_output(self, worker_class, md5, index_name, subfield):
        ''' Index worker output with the Indexer.
            Args:
                worker_class: 'strings', 'pe_features', whatever
                md5: the md5 of the sample
                index_name: the name of the index
                subfield: index just this subfield (None for all)
            Returns:
                Nothing
        '''

        # Grab the data
        if subfield:
            data = self.work_request(worker_class, md5)[worker_class][subfield]
        else:
            data = self.work_request(worker_class, md5)[worker_class]

        # Okay now index the data
        self.indexer.index_data(data, index_name=index_name, doc_type='unknown')

    def search(self, index_name, query):
        ''' Search a particular index in the Indexer
            Args:
                index_name: the name of the index
                query: the query against the index
            Returns:
                All matches to the query
        '''
        return self.indexer.search(index_name, query)

    #
    # Graph Methods
    #
    def add_node(self, node_id, name, labels):
        ''' Add a node to the graph with name and labels.
            Args:
                node_id: the unique node_id e.g. 'www.evil4u.com'
                name: the display name of the node e.g. 'evil4u'
                labels: a list of labels e.g. ['domain','evil']
            Returns:
                Nothing
        '''
        self.neo_db.add_node(node_id, name, labels)

    def has_node(self, node_id):
        ''' Does the Graph DB have this node
            Args:
                node_id: the unique node_id e.g. 'www.evil4u.com'
            Returns:
                True/False
        '''
        return self.neo_db.has_node(node_id)

    def add_rel(self, source_id, target_id, rel):
        ''' Add a relationship: source, target must already exist (see add_node)
            'rel' is the name of the relationship 'contains' or whatever.
            Args:
                source_id: the unique node_id of the source
                target_id: the unique node_id of the target
                rel: name of the relationship
            Returns:
                Nothing
        '''
        self.neo_db.add_rel(source_id, target_id, rel)

    def clear_graph_db(self):
        ''' Clear the Graph Database of all nodes and edges.
            Args:
                None
            Returns:
                Nothing
        '''
        self.neo_db.clear_db()

    def clear_db(self):
        ''' Clear the Main Database of all samples and worker output.
            Args:
                None
            Returns:
                Nothing
        '''
        self.data_store.clear_db()

    #
    # Work Request Methods
    #

    # Make a work request for an existing stored sample
    def work_request(self, worker_class, md5, subkeys=None):
        ''' Make a work request for an existing stored sample.
            Args:
                worker_class: 'strings', 'pe_features', whatever
                md5: the md5 of the sample
                index_name: the name of the index
                subkeys: just return a subfield e.g. 'foo' or 'foo.bar' (None for all) 
            Returns:
                The output of the worker or just the subfield of the worker output
        '''

        # Check valid
        if worker_class not in self.plugin_meta.keys():
            raise RuntimeError('Invalid work request for class %s (not found)' % (worker_class))

        # Get results (even if we have to wait for them)
        # Note: Yes, we're going to wait. Gevent concurrent execution will mean this
        #       code gets spawned off and new requests can be handled without issue.
        work_results = self._recursive_work_resolver(worker_class, md5)

        # Subkeys? (Fixme this is super klutzy)
        if subkeys:
            try:
                sub_results = {}
                for subkey in subkeys:
                    tmp = work_results[worker_class]
                    for key in subkey.split('.'):
                        tmp = tmp[key]
                        sub_results[key] = tmp
                work_results = sub_results
            except (KeyError, TypeError):
                raise RuntimeError('Could not get one or more subkeys for: %s' % (work_results))

        # Clean it and ship it
        work_results = self.data_store.clean_for_serialization(work_results)
        return work_results

    @zerorpc.stream
    def batch_work_request(self, worker_class, kwargs):
        ''' Make a batch work request for an existing set of stored samples.
            A subset of sample can be specified with kwargs.
            Args:
                worker_class: 'strings', 'pe_features', whatever
                kwargs: a way of specifying subsets of samples ({} for all)
                    type_tag: subset based on sample type (e.g. type_tag='pe')
                    md5_list: subset just the samples in this list
                    subkeys: return just this subkey (e.g. 'foo' or 'foo.bar')
            Returns:
                A generator that yields rows of worker output or subfields of the worker output
        '''
        type_tag = kwargs.get('type_tag',None)
        md5_list = kwargs.get('md5_list',None)
        subkeys = kwargs.get('subkeys',None)

        # If no md5_list specified put all samples (of type type_tag if not None)
        if not md5_list:
            md5_list = self.data_store.all_sample_md5s(type_tag) 

        # Loop through all the md5s and return a generator with yield
        for md5 in md5_list:
            try:
                if subkeys:
                    yield self.work_request(worker_class, md5, subkeys)
                else:
                    yield self.work_request(worker_class, md5)[worker_class]
            except KeyError:
                continue

    def store_sample_set(self, md5_list):
        ''' Store a sample set (which is just a list of md5s).
            Note: All md5s must already be in the data store.
            Args:
                md5_list: a list of the md5s in this set (all must exist in data store)
            Returns:
                The md5 of the set (the actual md5 of the set
        '''
        for md5 in md5_list:
            if not self.has_sample(md5):
                raise RuntimeError('Sample not found all items in sample_set\
                                    must be in the datastore: %s (not found)' % (md5))
        set_md5 = hashlib.md5(str(md5_list)).hexdigest()
        self._store_work_results({'md5_list':md5_list}, 'sample_set', set_md5)
        return set_md5

    def get_sample_set(self, md5):
        ''' Store a sample set (which is just a list of md5s).
            Args:
                md5_list: a list of the md5s in this set (all must exist in data store)
            Returns:
                The md5 of the set (the actual md5 of the set
        '''
        return self._get_work_results('sample_set', md5)

    @zerorpc.stream
    def stream_sample_set(self, md5):
        ''' Stream a sample set (which is just a list of md5s).
            Args:
                md5: the md5 of the sample_set
            Returns:
                A generator that yields the md5s in the sample set
        '''
        for md5 in self._get_work_results('sample_set', md5)['md5_list']:
            yield md5

    def get_datastore_uri(self):
        ''' Gives you the current datastore URL.
            Args:
                None
            Returns:
                The URI of the data store currently being used by Workbench
        '''
        return self.data_store.get_uri()

    def _new_plugin(self, plugin, mod_time):
        ''' The method handles the mechanics around new plugins. '''
        print '< %s: loaded >' % (plugin['name'])
        plugin['time_stamp'] = mod_time # datetime.datetime.utcnow()
        self.plugin_meta[plugin['name']] = plugin

    def _store_work_results(self, results, collection, md5):
        self.data_store.store_work_results(results, collection, md5)
    def _get_work_results(self, collection, md5):
        results = self.data_store.get_work_results(collection, md5)
        return {collection: results} if results else None


    # So the trick here is that since each worker just stores it's input dependencies
    # we can resursively backtrack and all the needed work gets done.
    def _recursive_work_resolver(self, worker_class, md5):

        # Looking for the sample or sample_set?
        if (worker_class == 'sample'):
            try:
                return self.get_sample(md5)
            except RuntimeError:
                return self.get_sample_set(md5)

        # Do I actually have this plugin? (might have failed, etc)
        if (worker_class not in self.plugin_meta):
            print 'Request for non-existing or failed plugin: %s' % (worker_class)
            return {}

        # If the results exist and the time_stamp is newer than the plugin's, I'm done
        collection = self.plugin_meta[worker_class]['name']
        work_results = self._get_work_results(collection, md5)
        if work_results:
            if self.plugin_meta[worker_class]['time_stamp'] < work_results[collection]['__time_stamp']:
                print 'Returning cached work results for plugin: %s' % (worker_class)
                return work_results
            else:
                print 'Updating work results for new plugin: %s' % (worker_class)

        dependencies = self.plugin_meta[worker_class]['dependencies']
        dependant_results = {}
        for dependency in dependencies:
            dependant_results.update(self._recursive_work_resolver(dependency, md5))
        print 'New work for plugin: %s' % (worker_class)
        work_results = self.plugin_meta[worker_class]['class']().execute(dependant_results)

        # Store the results and return
        self._store_work_results(work_results, collection, md5)
        return self._get_work_results(collection, md5)

    def _find_element(self,d,k):
        if k in d: return d[k]
        submatch = [d[_k][k] for _k in d if k in d[_k]]
        return submatch[0] if submatch else None

    def help(self):
        ''' Returns help commands '''

        help_str =  '\nWelcome to Workbench: Here\'s a list of help commands:'
        help_str += '\n\t - Run workbench.help_basic() for beginner help'
        help_str += '\n\t - Run workbench.help_commands() for command help'
        help_str += '\n\t - Run workbench.help_workers() for a list of workers'
        help_str += '\n\t - Run workbench.help_advanced() for advanced help'
        help_str += '\n\nSee https://github.com/SuperCowPowers/workbench for more information'
        return help_str

    def help_basic(self):
        ''' Returns basic help commands '''
        help_str =  '\nWorkbench: Getting started...'
        help_str += '\n\t - 1) $ print workbench.help_commands() for a list of commands'
        help_str += '\n\t - 2) $ print workbench.help_command(\'store_sample\') for into on a specific command'
        help_str += '\n\t - 3) $ print workbench.help_workers() for a list a workers'
        help_str += '\n\t - 4) $ print workbench.help_worker(\'meta\') for info on a specific worker'
        help_str += '\n\t - 5) $ my_md5 = workbench.store_sample(...)'
        help_str += '\n\t - 6) $ output = workbench.work_request(\'meta\', my_md5)'
        return help_str

    def help_commands(self):
        ''' Returns a big string of Workbench commands and signatures '''
        help_string = 'Workbench Commands:'
        for name, meth in inspect.getmembers(self, predicate=inspect.ismethod):
            if not name.startswith('_'):
                help_string += '\n\t%s%s' % (name,funcsigs.signature(meth))
        return help_string

    def help_command(self, command):
        ''' Returns a specific Workbench command and docstring '''
        for name, meth in inspect.getmembers(self, predicate=inspect.ismethod):
            if name == command:
                return '\n Command: %s%s \n%s' % (name, funcsigs.signature(meth), meth.__doc__)
        return '%s command not found.. misspelled?' % command

    def help_workers(self):
        ''' Returns a big string of the loaded Workbench workers and their dependencies '''
        help_string = 'Workbench Workers:'
        for name, plugin in sorted(self.plugin_meta.iteritems()):
            help_string += '\n\t%s %s' % (name, str(plugin['class'].dependencies))
        return help_string

    def help_worker(self, worker):
        ''' Returns a specific Workbench worker and docstring '''
        try:
            plugin = self.plugin_meta[worker]
            return '\n Worker: %s %s\n\t%s' % (worker, str(plugin['class'].dependencies), plugin['class'].__doc__)
        except KeyError:
            return '%s worker not found.. misspelled?' % worker

    def help_advanced(self):
        ''' Returns advanced help commands '''
        help_str =  '\nWoo! Advanced... <fixme: add documentation for advanced> :)'
        help_str += '\n\nSee https://github.com/SuperCowPowers/workbench for more information'
        return help_str

    def list_all_workers(self):
        ''' List all the currently loaded workers '''
        return self.plugin_meta.keys()

    def test_worker(self, worker):
        ''' Run the test for a specific worker '''

        # First find the plugin
        try:
            plugin = self.plugin_meta[worker]
        except KeyError:
            return '%s worker not found.. misspelled?' % worker

        # Now try to run the test
        try:
            plugin['test']()
            return True
        except (AttributeError, KeyError) as error:
            print 'Failure for plugin: %s' % (worker)
            print 'Error: %s' % error
            return False

def run():
    ''' Run the workbench server '''

    # Load the configuration file relative to this script location
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    workbench_conf = ConfigParser.ConfigParser()
    config_ini = workbench_conf.read(config_path)
    if not config_ini:
        print 'Could not locate config.ini file, tried %s : exiting...' % config_path
        exit(1)

    # Pull configuration settings
    datastore_uri = workbench_conf.get('workbench', 'datastore_uri')
    database = workbench_conf.get('workbench', 'database')
    worker_cap = workbench_conf.getint('workbench', 'worker_cap')
    samples_cap = workbench_conf.getint('workbench', 'samples_cap')

    # Spin up Workbench ZeroRPC
    try:
        store_args = {'uri': datastore_uri, 'database': database, 'worker_cap':worker_cap, 'samples_cap':samples_cap}
        workbench = zerorpc.Server(WorkBench(store_args=store_args), name='workbench')
        workbench.bind('tcp://0.0.0.0:4242')
        print 'ZeroRPC %s' % ('tcp://0.0.0.0:4242')
        gevent_signal(signal.SIGTERM, workbench.stop)
        gevent_signal(signal.SIGINT, workbench.stop)
        gevent_signal(signal.SIGKILL, workbench.stop)
        workbench.run()
        print '\nWorkbench Server Shutting Down...'
        exit(0)        
    except zmq.error.ZMQError:
        print '\nInfo: Could not start Workbench server (no worries, probably already running...)\n'


# Test that just calls main
def test():
    run()

if __name__ == '__main__':
    run()
