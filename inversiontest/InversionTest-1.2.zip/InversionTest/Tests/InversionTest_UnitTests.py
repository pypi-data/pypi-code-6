import unittest

class InversionTestTests(unittest.TestCase):
    PACKAGE_NAME = 'InversionTest'
    MODULE_NAMES = ('InversionAnalysis', 'InversionDistribution',
                    'StatisticalTests', 'PolynomialOperations')
    OBJECT_NAMES = ('SIMILARITY_METRIC', 'EXACT_CDF', 'NORMAL_CDF', 'ADAPTIVE_CDF', 'CDF_TYPES',
                    'GREATER_THAN_HYPOTHESIS', 'LESS_THAN_HYPOTHESIS',
                    'TWO_SIDED_HYPOTHESIS', 'TEST_HYPOTHESES',
                    'GradedPosetSequence', 'inversionCountMax', 'inversionCountMean', 'inversionCountVariance',
                    'medianSequence', 'inversionCount', 'mergeSortInversionCount', 'inversionSimilarity',
                    'inversionCountCDF', 'inversionSignTest', 'inversionWilcoxonTest',
                    'inversionPermutationMeanTest', 'inversionPermutationRankTest')

    def testPackageImport(self):
        try:
            __import__(self.PACKAGE_NAME)
        except ImportError:
            self.fail("Could not import main package: %s"%self.PACKAGE_NAME)
            
    def testModuleImports(self):
        failedImports = []
        for module in self.MODULE_NAMES:
            moduleName = self.PACKAGE_NAME + '.' + module
            try:
                __import__(moduleName)
            except ImportError:
                failedImports.append(moduleName)
        if len(failedImports) > 0:
            failStr = "Failed to load the following modules: %s"%(', '.join(failedImports),)
            self.fail(failStr)

    def testObjectImports_ImportFrom(self):
        failedImports = []
        packageName = self.PACKAGE_NAME
        for objectName in self.OBJECT_NAMES:
            try:
                __import__(packageName, fromlist=[objectName])
            except ImportError:
                failedImports.append(packageName + '.' + objectName)
        if len(failedImports) > 0:
            failStr = "Failed to load the following objects: %s"%(', '.join(failedImports),)
            self.fail(failStr)

    def testObjectImports_ImportRelative(self):
        failedImports = []
        packageName = self.PACKAGE_NAME
        for objectName in self.OBJECT_NAMES:
            InversionTest = __import__(packageName)
            objectRef = InversionTest.__package__ + '.' + objectName
            try:
                eval(objectRef)
            except NameError:
                failedImports.append(objectRef)
        if len(failedImports) > 0:
            failStr = "Failed to load the following objects: %s"%(', '.join(failedImports),)
            self.fail(failStr)

if __name__ == "__main__":
    unittest.main()
