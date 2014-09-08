from fileinput import input
from time import sleep
from pyes.exceptions import NoServerAvailable
import re


class Indexer:
    def __init__(self, client, batch_mode=True, batch_size=100):
        self.client = client
        self.batch_mode = batch_mode
        self.client.bulk_size = int(batch_size)

    def bulk_index(self, index, type, shapefile, sleep_time=0.1):
        print 'Indexing [%s] docs into [%s] from %s' % (type, index, shapefile)

        index_count = 0

        id_re = re.compile('^.*?"id"\s*:\s*"([^"]+)"')
        parens_re = re.compile('\(.*?\)')

        for line in input(shapefile):
            id = id_re.match(line).group(1)

            # cleanup any lines that contain parentheticals
            line = parens_re.sub('', line).strip()

            # sweet dec/encodings bro
            line = line.decode('latin-1').encode('utf-8')
            id = id.decode('latin-1').encode('utf-8')

            try:
                self.client.index(line, index, type, id, bulk=self.batch_mode)
            except UnicodeDecodeError as e:
                print "Error processing line with id %s: %s" % (id, e.message)
            except NoServerAvailable as e:
                print "The server failed to respond while indexing %s: [%s]. Sleeping %d seconds and retrying..." % (id, e.message, sleep_time)
                sleep(5)
                try:
                    print "Retrying indexing of %s" % id
                    self.client.index(line, index, type, id, bulk=self.batch_mode)
                except NoServerAvailable as e:
                    print "Failed to reconnect again. Skipping indexing %s" % id
                except Exception as e:
                    print "This happened: %s" % e

            index_count += 1
            if index_count % int(self.client.bulk_size) == 0:
                print 'Indexing batch of %d, starting from %s' % (self.client.bulk_size, id)
                sleep(sleep_time)

        # index remaining bulk entries
        self.client.force_bulk()