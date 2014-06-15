from warnings import catch_warnings
from tempfile import gettempdir
from os import unlink
from os.path import join, split
from unittest import TestCase, TestLoader, TextTestRunner, skipIf
from functools import partial
import sys

if __name__ == "__main__":
    from cobra import io
    from cobra.test import data_directory, create_test_model
    from cobra.test import ecoli_mat, ecoli_pickle, ecoli_json
    from cobra.test import salmonella_sbml, salmonella_pickle
    from cobra.test import salmonella_fbc_sbml
else:
    from .. import io
    from . import data_directory, create_test_model
    from . import ecoli_mat, ecoli_pickle, ecoli_json
    from . import salmonella_sbml, salmonella_pickle
    from . import salmonella_fbc_sbml

libraries = ["scipy", "libsbml"]
for library in libraries:
    try:
        exec("import %s" % library)
    except ImportError:
        exec("%s = None" % library)


class TestCobraIO(object):
    def compare_models(self, model1, model2):
        self.assertEqual(len(model1.reactions),
                         len(model2.reactions))
        self.assertEqual(len(model1.metabolites),
                         len(model2.metabolites))
        for attr in ("id", "name", "lower_bound", "upper_bound"):
            self.assertEqual(getattr(model1.reactions[0], attr),
                             getattr(model2.reactions[0], attr))
            self.assertEqual(getattr(model1.reactions[10], attr),
                             getattr(model2.reactions[10], attr))
            self.assertEqual(getattr(model1.reactions[-1], attr),
                             getattr(model2.reactions[-1], attr))
        for attr in ("id", "name"):
            self.assertEqual(getattr(model1.metabolites[0], attr),
                             getattr(model2.metabolites[0], attr))
            self.assertEqual(getattr(model1.metabolites[10], attr),
                             getattr(model2.metabolites[10], attr))
            self.assertEqual(getattr(model1.metabolites[-1], attr),
                             getattr(model2.metabolites[-1], attr))
        self.assertEqual(len(model1.reactions[0].metabolites),
                         len(model2.reactions[0].metabolites))
        self.assertEqual(len(model1.reactions[20].metabolites),
                         len(model2.reactions[20].metabolites))
        self.assertEqual(len(model1.reactions[-1].metabolites),
                         len(model2.reactions[-1].metabolites))
        # ensure they have the same solution max
        model1.optimize()
        model2.optimize()
        self.assertAlmostEqual(model1.solution.f, model2.solution.f,
                places=3)
    def test_read(self):
        #with catch_warnings(record=True) as w:
        read_model = self.read_function(self.test_file)
        self.compare_models(self.test_model, read_model)
   
    def test_read_nonexistent(self):
        # make sure that an error is raised when given a nonexistent file
        self.assertRaises(IOError, self.read_function, "fake_file")

    def test_write_and_reread(self):
        test_output_filename = join(gettempdir(), split(self.test_file)[-1])
        self.write_function(self.test_model, test_output_filename)
        #with catch_warnings(record=True) as w:
        reread_model = self.read_function(test_output_filename)
        self.compare_models(self.test_model, reread_model)
        unlink(test_output_filename)

@skipIf(not libsbml, "libsbml required")
class TestCobraIOSBML(TestCase, TestCobraIO):
    def setUp(self):
        self.test_model = create_test_model()
        self.test_file = salmonella_sbml
        self.read_function = io.read_sbml_model
        self.write_function = io.write_sbml_model

@skipIf(not libsbml, "libsbml required")
class TestCobraIOSBMLfbc(TestCase, TestCobraIO):
    def setUp(self):
        self.test_model = create_test_model()
        self.test_file = salmonella_fbc_sbml
        self.read_function = io.read_sbml_model
        self.write_function = partial(io.write_sbml_model,
                                      use_fbc_package=True)

@skipIf(not scipy, "scipy required")
class TestCobraIOmat(TestCase, TestCobraIO):
    def setUp(self):
        self.test_model = create_test_model(ecoli_pickle)
        self.test_file = ecoli_mat
        self.read_function = io.load_matlab_model
        self.write_function = io.save_matlab_model


class TestCobraIOjson(TestCase, TestCobraIO):
    def setUp(self):
        self.test_model = create_test_model(ecoli_pickle)
        self.test_file = ecoli_json
        self.read_function = io.load_json_model
        self.write_function = io.save_json_model

# make a test suite to run all of the tests
loader = TestLoader()
suite = loader.loadTestsFromModule(sys.modules[__name__])

def test_all():
    TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()
