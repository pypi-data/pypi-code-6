""" goulash.tests.data
"""

class TestObject(object):
    """ plain object with some misc stuff. """
    class_variable = 'foo'

    def _private_method(self): pass

    _private_method.test_attr='bar'

    @staticmethod
    def public_static_method(foo, bar): pass

    @property
    def _some_private_property(self):
        return 3

class ComplexTestObject(TestObject):
    """ this object has some inheritance!

        (that's useful for testing 'local' names.)
    """
    my_class_variable = 'foo'
