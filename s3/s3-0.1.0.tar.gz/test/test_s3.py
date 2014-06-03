import logging
import os
import random
import s3
import subprocess
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROGNAME = 'test_s3'
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
LOG_LEVEL = logging.DEBUG
YAML_FILENAME = os.path.normpath(os.path.join(BASE_DIR, '..', 's3.yaml'))

def create_file(filename, filesize):
    with open(filename, 'w') as fo:
        for i in range(1, filesize + 1):
            fo.write(chr(random.randint(0, 255)))

def delete_files(*filenames):
    for filename in filenames:
        if os.access(filename, os.F_OK):
            os.remove(filename)
            
def test_file(storage, filename, remote_name, local_name):
    headers = {
            'x-amz-meta-physics': "Kant",
            'x-amz-meta-carpal': "tunnel syndrome",
            'x-amz-meta-morphosis': "Kafka",
            }
    try:
        exists, metadata = storage.exists(remote_name)
        assert not exists
        storage.write(filename, remote_name, headers=headers)
        exists, metadata = storage.exists(remote_name)
        assert exists
        assert metadata == headers
        headers['x-amz-meta-morphosis'] += ', Franz'
        storage.update_metadata(remote_name, headers=headers)
        metadata = storage.read(remote_name, local_name)
        assert metadata == headers
        assert os.access(local_name, os.F_OK)
        storage.delete(remote_name)
        exists, metadata = storage.exists(remote_name)
        assert not exists
        assert 0 == subprocess.call(['diff', filename, local_name])
    except s3.StorageError, e:
        raise
        
def main():       
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)     

    with open(YAML_FILENAME, 'r') as fi:
        config = yaml.load(fi)

    connection = s3.S3Connection(**config['s3'])    
    storage = s3.Storage(connection)

    create_file('little', 10000)
    test_file(storage, 'little', 's3_little', 'from_s3_little')
    delete_files('little', 'from_s3_little')

    create_file('big', 123 + s3.S3Facts.multipart_threshhold * 1)
    test_file(storage, 'big', 's3_big', 'from_s3_big')
    delete_files('big', 'from_s3_big')

if __name__ == '__main__':
    main()

