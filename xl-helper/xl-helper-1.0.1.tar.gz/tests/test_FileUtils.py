import unittest

from xl_helper.FileUtils import FileUtils


class FileUtilsTest(unittest.TestCase):

    def test_proj_folder(self):
        proj_folder = FileUtils.proj_folder()
        assert proj_folder.endswith("xl-helper")

    def test_conf_folder(self):
        conf_folder = FileUtils.conf_folder()
        assert conf_folder.endswith("xl-helper/conf")

if __name__ == '__main__':
    unittest.main()