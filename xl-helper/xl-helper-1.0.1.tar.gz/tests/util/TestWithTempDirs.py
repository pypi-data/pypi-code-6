
import unittest
import tempfile
from xl_helper.FileUtils import FileUtils
from tests.util.TestingUtils import TestingUtils


class TestWithTempDirs(unittest.TestCase):

    default_temp = tempfile.mkdtemp()

    created_dirs = [default_temp]

    test_config = TestingUtils.get_test_config()

    @classmethod
    def tearDownClass(cls):
        super(TestWithTempDirs, cls).tearDownClass()
        for td in TestWithTempDirs.created_dirs:
            print("Removing temporary directory %s" % td)
            FileUtils.delete_dirs(td)

    def create_temp_dir(self):
        d = tempfile.mkdtemp()
        TestWithTempDirs.created_dirs.append(d)
        return d
