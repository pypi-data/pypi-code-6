import unittest
import InversionTest.Tests.InversionAnalysis_UnitTests as InversionAnalysis_UnitTests
import InversionTest.Tests.InversionDistribution_UnitTests as InversionDistribution_UnitTests
import InversionTest.Tests.InversionTest_UnitTests as InversionTest_UnitTests
import InversionTest.Tests.MonteCarloSampler_UnitTests as MonteCarloSampler_UnitTests
import InversionTest.Tests.PolynomialOperations_UnitTests as PolynomialOperations_UnitTests
import InversionTest.Tests.StatisticalTests_UnitTests as StatisticalTests_UnitTests

# Test Suite for InversionTest
# Note: If SciPy is not installed, 5 failure warnings are expected

def suite(aSuite=None):
    if aSuite is None:
        aSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    aSuite.addTests(loader.loadTestsFromModule(InversionAnalysis_UnitTests))
    aSuite.addTests(loader.loadTestsFromModule(InversionDistribution_UnitTests))
    aSuite.addTests(loader.loadTestsFromModule(InversionTest_UnitTests))
    aSuite.addTests(loader.loadTestsFromModule(MonteCarloSampler_UnitTests))
    aSuite.addTests(loader.loadTestsFromModule(PolynomialOperations_UnitTests))
    aSuite.addTests(loader.loadTestsFromModule(StatisticalTests_UnitTests))
    return aSuite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
