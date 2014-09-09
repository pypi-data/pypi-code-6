from testtools import TestCase
from mock import patch, DEFAULT


class MiscTest(TestCase):
    def test_get_client_info(self):
        from lacore import get_client_info, __version__
        self.assertEqual('lacore ' + __version__, get_client_info(True, False))
        self.assertEqual("Longaccess Python SDK " + __version__,
                         get_client_info(False, False))
        patches = ['platform', 'python_version', 'machine']
        kw = dict([(p, DEFAULT) for p in patches])
        with patch.multiple('platform', **kw) as mocks:
            expected = ["lacore", __version__]
            for p in patches:
                v = self.getUniqueString()
                expected.append("py" + v if p is "python_version" else v)
                mocks[p].return_value = v
            self.assertEqual(" ".join(expected), get_client_info(True, True))
            mocks['platform'].assert_called_with(True, True)
        with patch.multiple('platform', **kw) as mocks:
            expected = ["Longaccess Python SDK", __version__]
            for p in patches:
                v = self.getUniqueString()
                expected.append("py" + v if p is "python_version" else v)
                mocks[p].return_value = v
            self.assertEqual(" ".join(expected), get_client_info(False, True))
            mocks['platform'].assert_called_with(True, False)
