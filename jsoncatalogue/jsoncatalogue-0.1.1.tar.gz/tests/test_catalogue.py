from jsoncatalogue import Catalogue
import unittest
import os
from mock import Mock

class TestCatalogue(unittest.TestCase):
    def setUp(self):
        self.expected_keys = [
            "http://wordnik.github.io/schemas/v1.2/apiDeclaration.json",
            "http://wordnik.github.io/schemas/v1.2/infoObject.json",
            "http://wordnik.github.io/schemas/v1.2/authorizationObject.json",
            "http://wordnik.github.io/schemas/v1.2/modelsObject.json",
            "http://wordnik.github.io/schemas/v1.2/operationObject.json",
            "http://wordnik.github.io/schemas/v1.2/parameterObject.json",
            "http://wordnik.github.io/schemas/v1.2/dataTypeBase.json",
            "http://wordnik.github.io/schemas/v1.2/oauth2GrantType.json",
            "http://wordnik.github.io/schemas/v1.2/resourceObject.json",
            "http://wordnik.github.io/schemas/v1.2/dataType.json",
            "http://wordnik.github.io/schemas/v1.2/resourceListing.json"
        ]
        self.saved_dir = os.getcwd()
        self.test_home = "tests"
        self.catalogues_home = os.path.join(self.test_home, "data")
    def tearDown(self):
        os.chdir(self.saved_dir)
    def assertExpectedKeys(self, catalogue):
        for key in self.expected_keys:
            assert key in catalogue.store
    def cd_to_dir(self):
        """CD into tests dir and modifies path to catalogues"""
        newdir = "tests"
        os.chdir(newdir)
        self.catalogues_home = os.path.join("..", newdir, "data")
        return os.getcwd()

    def path_to(self, name):
        return os.path.join(self.catalogues_home, name)

    def test_catalogue_add_directory(self):
        catalogue = Catalogue()
        catalogue.add_directory(self.path_to("catalogue"))
        print catalogue.store.keys()
        self.assertExpectedKeys(catalogue)

    def test_catalogue_directdir(self):
        catalogue = Catalogue(self.path_to("catalogue"))
        print catalogue.store.keys()
        self.assertExpectedKeys(catalogue)

    def test_catalogue_dirupdown(self):
        rootdir = self.cd_to_dir()
        rootdir = self.path_to("catalogue")
        assert rootdir == "../tests/data/catalogue"
        catalogue = Catalogue(rootdir)
        print catalogue.store.keys()
        self.assertExpectedKeys(catalogue)


    def test_callback(self):
        mockcallback = Mock(return_value=None)
        catalogue = Catalogue(self.path_to("brokencatalogue"), mockcallback)
        assert mockcallback.called
        assert mockcallback.call_count == 1
        lastargs = mockcallback.call_args[0]
        print "lastargs", lastargs
        assert lastargs[0] == self.path_to("brokencatalogue")
        assert lastargs[1] == "http/google.com/broken.json"
        e = lastargs[2]
        assert isinstance(e, ValueError)
        assert e.message == "No JSON object could be decoded"

        print catalogue.store.keys()
        self.assertExpectedKeys(catalogue)
