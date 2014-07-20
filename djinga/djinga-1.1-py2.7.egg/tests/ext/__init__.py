from tests.tests import load_all


def load_tests(loader, standard_tests, pattern):
    return load_all(loader, __name__, __file__)
