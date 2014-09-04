import nose
import os

def runTests():
    r"""Run all tests"""
    cfd = os.path.dirname(os.path.realpath(__file__))
    nose.run(argv = [cfd,"--verbosity=2"])

if __name__ == "__main__":
    runTests()