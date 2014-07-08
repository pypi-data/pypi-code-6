
''' ELSIndexer class for WorkBench '''


class ELSIndexer(object):
    ''' ELSIndexer class for WorkBench '''

    def __init__(self, hosts=None):
        ''' Initialization for the Elastic Search Indexer '''

        # Set default value for hosts
        if not hosts:
            hosts = [{"host": "localhost", "port": 9200}]

        # Get connection to ElasticSearch
        try:
            self.els_search = elasticsearch.Elasticsearch(hosts)
            info = self.els_search.info()
            version = info['version']
            print 'ELS Indexer connected: %s %s %s %s' % (str(hosts), info['name'],
                                                          version['number'], version['lucene_version'])
        except elasticsearch.exceptions.ConnectionError:
            print 'ELS connection failed! Is your ELS server running?'
            exit(1)

    def index_data(self, data, index_name='meta', doc_type='unknown'):
        ''' Take an arbitrary dictionary of data and index it with ELS '''

        # Index the data (which needs to be a dict/object) if it's not
        # we're going to toss an exception
        if not isinstance(data, dict):
            raise RuntimeError('Index failed, data needs to be a dict!')

        try:
            self.els_search.index(index=index_name, doc_type=doc_type, body=data)
        except Exception, error:
            print 'Index failed: %s' % str(error)
            raise RuntimeError('Index failed: %s' % str(error))

    def search(self, index_name, query):
        ''' Search the given index_name with the given ELS query '''
        try:
            results = self.els_search.search(index=index_name, body=query)
            return results
        except Exception, error:
            error_str = 'Query failed: %s\n' % str(error)
            error_str += '\nIs there a dynamic script in the query?, see www.elasticsearch.org'
            print error_str
            raise RuntimeError(error_str)


class ELSStubIndexer(object):
    ''' ELS Stub '''

    def __init__(self, hosts='[{"host": "localhost", "port": 9200}]'):
        ''' Stub Indexer '''
        print 'ELS Stub Indexer connected: %s' % (str(hosts))
        print 'Install ElasticSearch and python bindings for ELS indexer. See README.md'
        print '%s %s' % (self, hosts)

    def index_data(self, data, index_name='meta', doc_type='unknown'):
        ''' Stub Indexer '''
        print 'ELS Stub Indexer getting called...'
        print '%s %s %s %s' % (self, data, index_name, doc_type)

    def search(self, index_name, query):
        ''' Stub Indexer '''
        print 'ELS Stub Indexer getting called...'
        print '%s %s %s' % (self, index_name, query)

try:
    import elasticsearch
    ELSIndexer = ELSIndexer
except ImportError:
    ELSIndexer = ELSStubIndexer
