
''' DataStore class for WorkBench '''

from gevent import monkey; monkey.patch_socket()
import pymongo
import gridfs
import hashlib
import datetime
import bson
import time


class DataStore(object):
    ''' DataStore for Workbench. Currently tied to MongoDB but making this class 'abstract' 
        should be straightforward and we could think about using another backend '''

    def __init__(self, uri='mongodb://localhost/workbench', database='workbench', worker_cap=0, samples_cap=0):
        ''' Initialization for the Workbench data store class '''
        
        self.sample_collection = 'samples'
        self.worker_cap = worker_cap
        self.samples_cap = samples_cap

        # Get connection to mongo
        self.database_name = database
        self.uri = 'mongodb://'+uri+'/'+self.database_name
        self.mongo = pymongo.MongoClient(self.uri, use_greenlets=True)
        self.database = self.mongo.get_default_database()

        # Get the gridfs handle
        self.gridfs_handle = gridfs.GridFS(self.database)

        # Run the periodic operations
        self.last_ops_run = time.time()
        self.periodic_ops()

        print 'WorkBench DataStore connected: %s:%s' % (self.uri, self.database_name)

    def get_uri(self):
        ''' Return the uri of the data store '''
        return self.uri

    def store_sample(self, filename, sample_bytes, type_tag):
        ''' Store a sample into the datastore '''

        sample_info = {}

        # Compute the MD5 hash
        sample_info['md5'] = hashlib.md5(sample_bytes).hexdigest()

        # Check if sample already exists
        if self.has_sample(sample_info['md5']):
            print 'Sample %s: already exists in DataStore' % (sample_info['md5'])
            return sample_info['md5']

        # Run the periodic operations
        self.periodic_ops()

        # Check if we need to expire anything
        self.expire_data()

        # Okay start populating the sample for adding to the data store
        # Filename, length, import time and type_tag
        sample_info['filename'] = filename
        sample_info['length'] = len(sample_bytes)
        sample_info['import_time'] = datetime.datetime.utcnow()
        sample_info['type_tag'] = type_tag

        # Random customer for now
        import random
        sample_info['customer'] = random.choice(['Mega Corp', 'Huge Inc', 'BearTron', 'Dorseys Mom'])

        # Push the file into the MongoDB GridFS
        sample_info['__grid_fs'] = self.gridfs_handle.put(sample_bytes)
        self.database[self.sample_collection].insert(sample_info)

        # Print info
        print 'Sample Storage: %.2f out of %.2f MB' % (self.sample_storage_size(), self.samples_cap)

        # Return the sample md5
        return sample_info['md5']

    def sample_storage_size(self):
        ''' Get the storage size of the samples storage collection '''
        try:
            coll_stats = self.database.command('collStats', 'fs.chunks')
            sample_storage_size = coll_stats['size']/1024.0/1024.0
            return sample_storage_size
        except pymongo.errors.OperationFailure:
            return 0

    def expire_data(self):
        ''' Expire data within the samples collection '''

        # Do we need to start deleting stuff?
        while self.sample_storage_size() > self.samples_cap:

            # This should return the 'oldest' record in samples
            record = self.database[self.sample_collection].find().sort('import_time',pymongo.ASCENDING).limit(1)[0]

            # Delete it
            print 'Deleting sample: %s (%.2f MB)...' % (record['md5'], record['length']/1024.0/1024.0)
            self.database[self.sample_collection].remove({'md5': record['md5']})
            self.gridfs_handle.delete(record['__grid_fs'])

            # Print info
            print 'Sample Storage: %.2f out of %.2f MB' % (self.sample_storage_size(), self.samples_cap)

    def clean_for_serialization(self, data):
        ''' Clean data in preparation for serialization '''
        if isinstance(data, dict):
            for k in data.keys():
                if (k.startswith('__')): 
                    del data[k]
                elif isinstance(data[k], bson.objectid.ObjectId): 
                    del data[k]
                elif isinstance(data[k], datetime.datetime):
                    data[k] = data[k].isoformat()+'Z'
                elif isinstance(data[k], dict):
                    data[k] = self.clean_for_serialization(data[k])
                elif isinstance(data[k], list):
                    data[k] = [self.clean_for_serialization(item) for item in data[k]]
        return data

    def clean_for_storage(self, data):
        ''' Clean data in preparation for storage '''
        data = self.data_to_unicode(data)
        if isinstance(data, dict):
            for k in dict(data).keys():
                if k == '_id':
                    del data[k]
                    continue
                if '.' in k:
                    new_k = k.replace('.', '_')
                    data[new_k] = data[k]
                    del data[k]
                    k = new_k
                if isinstance(data[k], dict):
                    data[k] = self.clean_for_storage(data[k])
                elif isinstance(data[k], list):
                    data[k] = [self.clean_for_storage(item) for item in data[k]]
        return data

    def get_sample(self, md5):
        ''' Get the sample from the data store '''
        sample_info = self.database[self.sample_collection].find_one({'md5': md5})
        if not sample_info:
            raise RuntimeError('Sample not found: %s ' % (md5))

        # Get the raw bytes from GridFS (note: this could fail)
        try:
            grid_fs_id = sample_info['__grid_fs']
            sample_info = self.clean_for_serialization(sample_info)
            sample_info.update({'raw_bytes':self.gridfs_handle.get(grid_fs_id).read()})
            return sample_info
        except gridfs.errors.CorruptGridFile:
            # If we don't have the gridfs files, delete the entry from samples
            self.database[self.sample_collection].update({'md5': md5}, {'md5': None})
            raise RuntimeError('Sample not found: %s ' % (md5))

    def get_sample_window(self, type_tag, size=10):
        ''' Get a window of samples not to exceed size (in MB) '''

        # Convert size to MB
        size = size * 1024 * 1024

        # Grab all the samples of type=type_tag, sort by import_time (newest to oldest)
        cursor = self.database[self.sample_collection].find({'type_tag': type_tag},
            {'md5': 1,'length': 1}).sort('import_time',pymongo.DESCENDING)
        total_size = 0
        md5_list = []
        for item in cursor:
            if total_size > size:
                return md5_list
            md5_list.append(item['md5'])
            total_size += item['length']

        # If you get this far you don't have 'size' amount of data
        # so just return what you've got
        return md5_list

    def has_sample(self, md5):
        ''' See if the data store has this sample '''

        # The easiest thing is to simply get the sample and if that
        # succeeds than return True, else return False
        try:
            self.get_sample(md5)
            return True
        except RuntimeError:
            return False

    def store_work_results(self, results, collection, md5):
        ''' Store the output results of the worker '''
        results['md5'] = md5
        results['__time_stamp'] = datetime.datetime.utcnow()

        # Fixme: Occasionally a capped collection will not let you update with a 
        #        larger object, if you have MongoDB 2.6 or above this shouldn't
        #        really happen, so for now just kinda punting and giving a message.
        try:
            self.database[collection].update({'md5':md5}, self.clean_for_storage(results), True)
        except pymongo.errors.OperationFailure:
            print 'Not updating exising object in capped collection...(upgrade to mongodb 2.6)'

    def get_work_results(self, collection, md5):
        ''' Get the results of the worker '''
        return self.database[collection].find_one({'md5':md5})

    def all_sample_md5s(self, type_tag=None):
        ''' Return a list of all md5 matching the type_tag ('pe','pdf', etc). '''
        if type_tag:
            cursor = self.database[self.sample_collection].find({'type_tag': type_tag}, {'md5': 1, '_id': 0})
        else:
            cursor = self.database[self.sample_collection].find({}, {'md5': 1, '_id': 0})
        return [match.values()[0] for match in cursor]

    def clear_db(self):
        ''' Drop the entire workbench database... Whee! '''
        print 'Dropping the entire workbench database... Whee!'
        self.mongo.drop_database(self.database_name)

    def periodic_ops(self):
        ''' Run periodic operations on the the data store
            Things like making sure collections are capped
            and indexes are set up '''

        # Only run every 5 minutes
        if (time.time() - self.last_ops_run) < 300:
            return

        # Reset last ops run
        self.last_ops_run = time.time()
        print 'Running Periodic Ops'

        # Get all the collections in the workbench database
        all_c = self.database.collection_names()

        # Remove collections that we don't want to cap
        try:
            all_c.remove('system.indexes')
            all_c.remove('fs.chunks')
            all_c.remove('fs.files')
            all_c.remove(self.sample_collection)
        except ValueError:
            print 'Catching a benign exception thats expected...'

        # Convert collections to capped if desired
        if self.worker_cap:
            size = self.worker_cap * pow(1024, 2)  # MegaBytes per collection
            for collection in all_c:
                self.database.command('convertToCapped', collection, size=size)

        # Loop through all collections ensuring they have an index on MD5s
        for collection in all_c:
            self.database[collection].ensure_index('md5')

        # Add required index for samples collection
        self.database[self.sample_collection].create_index('import_time')

    # Helper functions
    def to_unicode(self, s):
        ''' Convert an elementary datatype to unicode '''

        # Fixme: This is total horseshit
        if isinstance(s, unicode):
            return s
        if isinstance(s, str):
            return unicode(s, errors='ignore')

        # Just return the original object
        return s

    def data_to_unicode(self, data):
        ''' Recursively convert a list or dictionary to unicode '''
        if isinstance(data, dict):
            return {self.to_unicode(k): self.to_unicode(v) for k, v in data.iteritems()}
        if isinstance(data, list):
            return [self.to_unicode(l) for l in data]
        else:
            return self.to_unicode(data)
