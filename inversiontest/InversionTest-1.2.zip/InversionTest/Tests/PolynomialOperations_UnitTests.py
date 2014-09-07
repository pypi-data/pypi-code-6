import unittest
import random
import InversionTest.PolynomialOperations as PolynomialOperations

class PolynomialOperationsTests(unittest.TestCase):
    def testExpansionReversal(self):
        """ Test a random number of monic polynomial expansions and ensure they reduce properly """
        numTests = 100
        randint = random.randint
        polynomialExpansion = PolynomialOperations.polynomialExpansion
        syntheticDivision = PolynomialOperations.syntheticDivision
        for i in xrange(numTests):
            randint = random.randint
            numLists = randint(1,6)
            coeffLens = [randint(0, 3) for i in xrange(numLists)]
            coeffs = [[1] + [randint(-20,20) for i in xrange(1,aLen)] for aLen in coeffLens]
            exp = polynomialExpansion(*coeffs)
            for coeff in coeffs:
                oldExp = exp
                exp, remainder = syntheticDivision(exp, coeff)
                self.assertEqual(sum(remainder), 0)
            self.assertTrue(sum(exp) == 1 and exp[0] == 1)

    def testExpansion_Null(self):
        polynomialExpansion = PolynomialOperations.polynomialExpansion
        self.assertEqual(polynomialExpansion(), [])

    def testExpansion_Empty(self):
        polynomialExpansion = PolynomialOperations.polynomialExpansion
        self.assertEqual(polynomialExpansion([]), [])
        self.assertEqual(polynomialExpansion([],[]), [])
        self.assertEqual(polynomialExpansion([1,1,1],[]), [])
        self.assertEqual(polynomialExpansion([],[1,1,1]), [])

    def testExpansion_Identity(self):
        polynomialExpansion = PolynomialOperations.polynomialExpansion
        x = [1,0,1,4,6]
        self.assertEqual(polynomialExpansion(x), x)

    def testExpansion_Square(self):
        polynomialExpansion = PolynomialOperations.polynomialExpansion
        x = [2,1,5]
        answer = [4,4,21,10,25]
        self.assertEqual(polynomialExpansion(x,x), answer)

    def testExpansion_Uneven(self):
        polynomialExpansion = PolynomialOperations.polynomialExpansion
        x = [1,-1,-3]
        y = [-1,10,5,13,0,1]
        answer = [-1,11,-2,-22,-28,-38,-1,-3]
        self.assertEqual(polynomialExpansion(x,y), answer)

    def testSyntheticDivision_Null(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        self.assertEqual(polynomialExpansion([],[]), ([],[]))

    def testSyntheticDivision_DenomEmpty(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        numerator = [1,2,3]
        divisor = []
        result = (numerator,[])
        self.assertEqual(polynomialExpansion(numerator, divisor), result)

    def testSyntheticDivision_NumEmpty(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        numerator = []
        divisor = [1,2,3]
        result = ([],numerator)
        self.assertEqual(polynomialExpansion(numerator, divisor), result)

    def testSyntheticDivision_NumSmaller(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        numerator = [10,4]
        divisor = [1,2,3]
        result = ([],numerator)
        self.assertEqual(polynomialExpansion(numerator, divisor), result)

    def testSyntheticDivision_Indivisible(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        numerator = [1,0,0]
        divisor = [1,7,7]
        result = ([],numerator)
        self.assertEqual(polynomialExpansion(numerator, divisor), result)

    def testSyntheticDivision_Partial(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        numerator = [1,2,2,1]
        divisor = [1,2,1]
        result = ([1,0],[1,1])
        self.assertEqual(polynomialExpansion(numerator, divisor), result)

    def testSyntheticDivision_Double(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        numerator = [2,2,2]
        divisor = [1,1,1]
        result = ([2],[0,0])
        self.assertEqual(polynomialExpansion(numerator, divisor), result)

    def testSyntheticDivision_Total(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        numerator = [1,2,2,1]
        divisor = [1,1,1]
        result = ([1,1],[0,0])
        self.assertEqual(polynomialExpansion(numerator, divisor), result)

    def testSyntheticDivision_TotalBig(self):
        polynomialExpansion = PolynomialOperations.syntheticDivision
        numerator = [1,3,5,6,5,3,1]
        divisor = [1,1,1,1]
        result = ([1,2,2,1],[0,0,0])
        self.assertEqual(polynomialExpansion(numerator, divisor), result)

        
if __name__ == "__main__":
    unittest.main()
