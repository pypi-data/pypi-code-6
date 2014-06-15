import os
import shutil
import datetime

from __setup import TestCase

import time
import whisper
from graphite import settings
from graphite import query
from pprint import pprint

class QueryTest(TestCase):
    _test_data = [0.5, 0.4, 0.6]

    def setUp(self):
        super(QueryTest, self).setUp()
        settings.CREATE_DIRECTORIES = False
        if not os.path.exists(settings.WHISPER_DIR):
            os.makedirs(settings.WHISPER_DIR)
        if not settings.STANDARD_DIRS:
            raise Exception("settings.STANDARD_DIRS shouldn't be empty")
        self.populate_data()

    def populate_data(self):
        self.db = os.path.join(settings.WHISPER_DIR, 'test.wsp')
        whisper.create(self.db, [(1, 60)])
        ts = int(time.time())
        for i, value in enumerate(reversed(self._test_data)):
            whisper.update(self.db, value, ts - i)
        self.ts = ts

    def test_generate_and_query_data(self):
        data = query.query(**{'target': 'test'})
        end = data[0]#[-4:]
        match = False
        # We iterate through all values and check
        # _test_data against 3 consecutive values
        # because sometimes whisper adds None
        # value(s) to the end (depending on time)
        for i, value in enumerate(end):
            if value == self._test_data[0]:
                self.assertEqual(end[i:i+3], self._test_data)
                match = True
                break
        self.assertTrue(match)

    def test_params_type(self):
        self.assertRaises(TypeError, query.query, {"localhost.service"})

    def test_all_None(self):
        whisper.create(os.path.join(settings.WHISPER_DIR, 'test_all_None.wsp'), [(1, 60)])
        data = query.query(**{'target': 'test_all_None'})
        self.assertNotEqual(data, [])

    def test_change_STANDARD_DIRS(self):
        " A test against a bug that was found in StandardFinder.directories "
        # This sets up whatever was the default storage directory layout
        # We remove the default storage dir
        shutil.rmtree(settings.STORAGE_DIR, ignore_errors=True)
        # Now change the storage directory
        STORAGE_DIR_new = settings.STORAGE_DIR + '_new'
        # Remove if exists
        shutil.rmtree(STORAGE_DIR_new, ignore_errors=True)
        settings.setup_storage_variables(STORAGE_DIR_new, create_directories=True)
        self.populate_data()
        data = query.query(**{'target': 'test'})
        self.assertTrue(data[0])

    def test_positional_arguments(self):
        Q = query.query
        self.assertTrue(Q('test'))
        # Because of the passing of time (not sure though)
        # we check three values, as graphite may not return 60 as hoped
        self.assertIn(len(list(Q('test')[0])), (59, 60, 61))
        # res = Q('test', '-3min')[0]
        # pprint([(attr, getattr(res, attr)) for attr in dir(res) if not attr.startswith("_")])
        # print datetime.datetime.fromtimestamp(res.start)
        # print datetime.datetime.fromtimestamp(res.end)
        # print (res.end - res.start), 'seconds'
        # print res.count()
        # self.assertEqual(len(list(res)), 60)

    def test_old_whisper_data(self):
        wsp_file = os.path.join(settings.WHISPER_DIR, 'test.wsp')
        current_time = os.stat(wsp_file).st_mtime

        # Now, modify the modification time to be one day old
        old_time = current_time - 60*60*24
        os.utime(wsp_file, (old_time, old_time))
        data = query.query(**{'target': 'test'})
        # This test fails on purpose, as it's unsure whether it's a bug or
        # a feature
        self.assertNotEqual(data, [])

    def test_get_all_leaf_nodes(self):
        # Create another "node" so there are two nodes
        whisper.create(os.path.join(settings.WHISPER_DIR, 'test_all_None.wsp'), [(1, 60)])
        nodes = query.get_all_leaf_nodes()
        self.assertEqual(sorted(nodes), sorted(['test', 'test_all_None']))

    def test_eval_qs(self):
        self.assertEqual(query.query('test'),
                         query.eval_qs('"format=raw&target=test"'))