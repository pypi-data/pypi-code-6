import unittest.mock
import os
import pkg_resources
import tornado.testing
import jazz


class TestCase(tornado.testing.AsyncHTTPTestCase,
               tornado.testing.LogTrapTestCase):

    def get_app(self):
        return jazz.Application()


class MainTest(TestCase):

    main = staticmethod(pkg_resources.load_entry_point(
        "devbliss-jazz", "console_scripts", "jazz"))

    @unittest.mock.patch("jazz.Application.listen")
    def test_main(self, listen):
        ioloop = unittest.mock.Mock()
        self.main(["--debug"], ioloop=ioloop)
        listen.assert_called_once_with(port="3000")
        ioloop.start.assert_called_once()

    @unittest.mock.patch("jazz.Application.listen")
    def test_main_exit(self, listen):
        ioloop = unittest.mock.Mock()
        ioloop.start.side_effect = KeyboardInterrupt()
        self.assertEqual(self.main([], ioloop=ioloop), 1)

    @unittest.mock.patch("builtins.print")
    def test_main_args(self, _):
        self.assertEqual(self.main(["--invalid-option"]), 2)

    @unittest.mock.patch("builtins.print")
    def test_main_help(self, _):
        self.assertEqual(self.main(["--help"]), 0)


class DistributionTest(TestCase):

    dist = pkg_resources.get_distribution("devbliss-jazz")

    def test_version(self):
        self.assertEqual(jazz.__version__, self.dist.version)
        self.assertRegex(jazz.__version__, r'\d+\.\d+\.\d+')

    def test_package_data(self):
        def tree(directory):
            for path, dirs, files in os.walk(directory):
                for i in (os.path.join(path, i) for i in files):
                    yield i
        sources = list(self.dist.get_metadata_lines("SOURCES.txt"))
        for directory, _ in (os.path.split(i) for i in sources):
            for f in tree(directory):
                (self.fail("Untracked file in distribution: " + f)
                 if f not in sources
                 and not f.endswith(".pyc")
                 and not f.endswith(".py") else None)
