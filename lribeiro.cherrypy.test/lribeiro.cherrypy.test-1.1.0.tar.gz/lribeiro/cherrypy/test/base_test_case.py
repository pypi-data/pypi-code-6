import unittest
import warnings


def _camelize(word, first_upper=False):
    camelized = ''.join(x.capitalize() for x in word.split('_'))
    if not first_upper:
        camelized = camelized[0].lower() + camelized[1:]
    return camelized


def def_if_has_camelcase(method):
    if hasattr(unittest.TestCase, _camelize(method.__name__)):
        return method


class BasePythonicTestCase(unittest.TestCase):
    @def_if_has_camelcase
    def sub_test(self, msg=None, **params):
        return self.subTest(msg, **params)
    if sub_test:
        sub_test.__test__ = False  # required to tell nose to not treat this like a test function

    def skip_test(self, reason):
        self.skipTest(reason)
    skip_test.__test__ = False

    @property
    def failure_exception(self):
        return self.failureException

    # def long_message
    if hasattr(unittest.TestCase, 'longMessage'):
        @property
        def long_message(self):
            return self.longMessage

        @long_message.setter
        def long_message(self, value):
            self.longMessage = value

    # def max_diff
    if hasattr(unittest.TestCase, 'maxDiff'):
        @property
        def max_diff(self):
            return self.maxDiff

        @max_diff.setter
        def max_diff(self, value):
            self.maxDiff = value

    def count_test_cases(self):
        return self.countTestCases()
    count_test_cases.__test__ = False

    def default_test_result(self):
        return self.defaultTestResult()
    default_test_result.__test__ = False

    def short_description(self):
        return self.shortDescription()

    @def_if_has_camelcase
    def add_cleanup(self, function, *args, **kwargs):
        self.addCleanup(function, *args, **kwargs)

    @def_if_has_camelcase
    def do_cleanups(self):
        self.doCleanups()

    @def_if_has_camelcase
    def add_type_equality_func(self, typeobj, function):
        self.addTypeEqualityFunc(typeobj, function)

    import sys
    if sys.version_info >= (3,):
        def _addSkip(self, result, test_case, reason):
            add_skip = getattr(result, 'add_skip', None)
            if add_skip is not None:
                add_skip(test_case, reason)
            else:
                warnings.warn("TestResult has no add_skip method, skips not reported",
                              RuntimeWarning, 2)
                result.addSuccess(test_case)
    else:
        def _addSkip(self, result, reason):
            addSkip = getattr(result, 'addSkip', None)
            if addSkip is not None:
                addSkip(self, reason)
            else:
                warnings.warn("TestResult has no addSkip method, skips not reported",
                              RuntimeWarning, 2)
                result.addSuccess(self)


class PythonicTestCase(BasePythonicTestCase):
    """
    Exposes unittest.TestCase methods in a pythonic syntax
    """

    def assert_equal(self, first, second, msg=None):
        self.assertEqual(first, second, msg)

    def assert_not_equal(self, first, second, msg=None):
        self.assertNotEqual(first, second, msg)

    def assert_true(self, expr, msg=None):
        self.assertTrue(expr, msg)

    def assert_false(self, expr, msg=None):
        self.assertFalse(expr, msg)

    @def_if_has_camelcase
    def assert_is(self, expr1, expr2, msg=None):
        self.assertIs(expr1, expr2, msg)

    @def_if_has_camelcase
    def assert_is_not(self, expr1, expr2, msg=None):
        self.assertIsNot(expr1, expr2, msg)

    @def_if_has_camelcase
    def assert_is_none(self, obj, msg=None):
        self.assertIsNone(obj, msg)

    @def_if_has_camelcase
    def assert_is_not_none(self, obj, msg=None):
        self.assertIsNotNone(obj, msg)

    @def_if_has_camelcase
    def assert_in(self, member, container, msg=None):
        self.assertIn(member, container, msg)

    @def_if_has_camelcase
    def assert_not_in(self, member, container, msg=None):
        self.assertNotIn(member, container, msg)

    @def_if_has_camelcase
    def assert_is_instance(self, obj, cls, msg=None):
        self.assertIsInstance(obj, cls, msg)

    @def_if_has_camelcase
    def assert_not_is_instance(self, obj, cls, msg=None):
        self.assertNotIsInstance(obj, cls, msg)

    # Method that checks the productions of exceptions
    def assert_raises(self, exc_class, callable_obj=None, *args, **kwargs):
        self.assertRaises(exc_class, callable_obj, *args, **kwargs)

    @def_if_has_camelcase
    def assert_raises_regex(self, expected_exception, expected_regex, callable_obj=None, *args, **kwargs):
        return self.assertRaisesRegex(expected_exception, expected_regex, callable_obj, *args, **kwargs)

    @def_if_has_camelcase
    def assert_warns(self, expected_warning, callable_obj=None, *args, **kwargs):
        self.assertWarns(expected_warning, callable_obj, *args, **kwargs)

    @def_if_has_camelcase
    def assert_warns_regex(self, expected_warning, expected_regex, callable_obj=None, *args, **kwargs):
        return self.assertWarnsRegex(expected_warning, expected_regex, callable_obj, *args, **kwargs)

    @def_if_has_camelcase
    def assert_logs(self, logger=None, level=None):
        return self.assertLogs(logger, level)

    # Methods to perform specific checks
    @def_if_has_camelcase
    def assert_almost_equal(self, first, second, places=None, msg=None, delta=None):
        self.assertAlmostEqual(first, second, places, msg, delta)

    @def_if_has_camelcase
    def assert_not_almost_equal(self, first, second, places=None, msg=None, delta=None):
        self.assertNotAlmostEqual(first, second, places, msg, delta)

    @def_if_has_camelcase
    def assert_greater(self, a, b, msg=None):
        self.assertGreater(a, b, msg)

    @def_if_has_camelcase
    def assert_greater_equal(self, a, b, msg=None):
        self.assertGreaterEqual(a, b, msg)

    @def_if_has_camelcase
    def assert_less(self, a, b, msg=None):
        self.assertLess(a, b, msg)

    @def_if_has_camelcase
    def assert_less_equal(self, a, b, msg=None):
        self.assertLessEqual(a, b, msg)

    @def_if_has_camelcase
    def assert_regex(self, text, expected_regex, msg=None):
        return self.assertRegex(text, expected_regex, msg)

    @def_if_has_camelcase
    def assert_not_regex(self, text, unexpected_regex, msg=None):
        return self.assertNotRegex(text, unexpected_regex, msg)

    @def_if_has_camelcase
    def assert_count_equal(self, first, second, msg=None):
        self.assertCountEqual(first, second, msg)

    @def_if_has_camelcase
    def assert_multi_line_equal(self, first, second, msg=None):
        self.assertMultiLineEqual(first, second, msg)

    @def_if_has_camelcase
    def assert_sequence_equal(self, seq1, seq2, msg=None, seq_type=None):
        self.assertSequenceEqual(seq1, seq2, msg, seq_type)

    @def_if_has_camelcase
    def assert_list_equal(self, list1, list2, msg=None):
        self.assertListEqual(list1, list2, msg)

    @def_if_has_camelcase
    def assert_tuple_equal(self, tuple1, tuple2, msg=None):
        self.assertTupleEqual(tuple1, tuple2, msg)

    @def_if_has_camelcase
    def assert_set_equal(self, set1, set2, msg=None):
        self.assertSetEqual(set1, set2, msg)

    @def_if_has_camelcase
    def assert_dict_equal(self, d1, d2, msg=None):
        self.assertDictEqual(d1, d2, msg)