from unittest import TestCase
from uuid import UUID

import mock

from quant.dependencygraph import createModelledFunction, registry, \
    ModelledFunction, sum_a_b
from __init__ import createCallRequirement, CallRequirement, createUuid, DependencyGraphRunner, createResult


__author__ = 'john'


class BaseTestCase(TestCase):

    def _create_call_requirement(self, required_calls):
        modelled_func = self._create_mock_modelled_function(return_value=10)
        registry.functions[modelled_func.id] = modelled_func
        c = createCallRequirement(
            stubbedExprStr=modelled_func,
            requiredStubIds=required_calls,
        )
        return c

    def _create_mock_modelled_function(self, return_value):
        modelled_func = mock.Mock()
        modelled_func.id = createUuid()
        modelled_func.call_modified.return_value = return_value
        if not isinstance(modelled_func, ModelledFunction):
            ModelledFunction.register(mock.Mock)  # An abc thing: allows Mock to pass isinstance checks.
        assert isinstance(modelled_func, ModelledFunction)
        return modelled_func


class TestResult(BaseTestCase):

    def test_create_result(self):
        self.r = createResult(callRequirementId=UUID(int=1), returnValue=10)
        self.assertEqual(self.r.id, UUID(int=1))
        self.assertEqual(self.r.value, 10)
        self.assertIn(self.r.id, registry.results)
        self.assertEqual(registry.results[self.r.id], self.r)

    def tearDown(self):
        registry.results.pop(self.r.id)


class TestRunner(BaseTestCase):

    def test_get_required_calls(self):
        c1 = self._create_call_requirement(required_calls=[])
        c2 = self._create_call_requirement(required_calls=[])
        c3 = self._create_call_requirement(required_calls=[c1.id, c2.id])
        c4 = self._create_call_requirement(required_calls=[])
        c5 = self._create_call_requirement(required_calls=[c3.id, c4.id])
        c6 = self._create_call_requirement(required_calls=[c5.id])
        runner = DependencyGraphRunner(c6.id)
        self.assertEqual(len(runner.getRequiredCalls(c1.id)), 1)
        self.assertEqual(len(runner.getRequiredCalls(c2.id)), 1)
        self.assertEqual(len(runner.getRequiredCalls(c3.id)), 3)
        self.assertEqual(len(runner.getRequiredCalls(c4.id)), 1)
        self.assertEqual(len(runner.getRequiredCalls(c5.id)), 5)
        self.assertEqual(len(runner.getRequiredCalls(c6.id)), 6)

    def test_execute_leaf(self):
        c1 = self._create_call_requirement(required_calls=[])
        runner = DependencyGraphRunner(c1.id)
        self.assertNotIn(c1.id, registry.results)
        runner.run()
        self.assertIn(c1.id, registry.results)
        result = registry.results[c1.id]
        self.assertEqual(result.value, 10)

    def test_execute_tree(self):
        c1 = self._create_call_requirement(required_calls=[])
        c2 = self._create_call_requirement(required_calls=[])
        c3 = self._create_call_requirement(required_calls=[c1.id, c2.id])
        c4 = self._create_call_requirement(required_calls=[])
        c5 = self._create_call_requirement(required_calls=[c3.id, c4.id])
        runner = DependencyGraphRunner(c5.id)
        self.assertNotIn(c5.id, registry.results)
        runner.run()
        self.assertIn(c5.id, registry.results)


class TestCallRequirement(BaseTestCase):

    def test_create_call_requirement(self):
        c = self._create_call_requirement(required_calls=[])
        assert isinstance(c, CallRequirement)
        self.assertTrue(c.id)
        self.assertTrue(c.stubbedExprStr)
        self.assertIsInstance(c.requiredCallIds, list)
        self.assertFalse(c.requiredCallIds)
        self.assertIsInstance(c.subscribers, list)
        self.assertFalse(c.subscribers)
        self.assertIsInstance(c.orig_arg_values, list)
        self.assertIsInstance(c.augm_arg_values, list)
        self.assertEqual(len(c.requiredCallIds), len(c.augm_arg_values))

        c1 = self._create_call_requirement(required_calls=[c.id])
        self.assertIsInstance(c1.required_calls, list)
        self.assertEqual(len(c1.required_calls), 1)
        self.assertIn(c.id, c1.required_calls)
        self.assertEqual(len(c.subscribers), 1)
        self.assertIn(c1.id, c.subscribers)
        self.assertEqual(len(c.requiredCallIds), len(c.augm_arg_values))

        c1 = self._create_call_requirement(required_calls=[])
        c2 = self._create_call_requirement(required_calls=[])
        c3 = self._create_call_requirement(required_calls=[c1.id, c2.id])
        c4 = self._create_call_requirement(required_calls=[])
        c5 = self._create_call_requirement(required_calls=[c3.id, c4.id])
        self.assertIn(c3.id, c1.subscribers)
        self.assertIn(c3.id, c2.subscribers)
        self.assertIn(c5.id, c4.subscribers)
        self.assertIn(c5.id, c3.subscribers)

    def test_is_ready(self):
        # No call requirements.
        c = self._create_call_requirement(required_calls=[])
        assert isinstance(c, CallRequirement)
        self.assertTrue(c.isReady())

        # One call requirement.
        c0 = self._create_call_requirement(required_calls=[])
        c1 = self._create_call_requirement(required_calls=[c0.id])
        assert isinstance(c1, CallRequirement)
        self.assertFalse(c1.isReady())
        c1.store_required_value(call_requirement_id=c0.id, return_value=10)
        self.assertTrue(c1.isReady())

        # Two call requirements.
        c0 = self._create_call_requirement(required_calls=[])
        c1 = self._create_call_requirement(required_calls=[])
        c2 = self._create_call_requirement(required_calls=[c0.id, c1.id])
        assert isinstance(c2, CallRequirement)
        self.assertFalse(c2.isReady())
        c2.store_required_value(call_requirement_id=c0.id, return_value=10)
        self.assertFalse(c2.isReady())
        c2.store_required_value(call_requirement_id=c1.id, return_value=20)
        self.assertTrue(c2.isReady())


class TestModelledFunction(TestCase):

    def test_create_modelled_function(self):
        f = createModelledFunction(modified_func_def=lambda arg_values: arg_values[0])
        self.assertTrue(f.id)
        self.assertEqual(f.evaluate(arg_values=[10]), 10)

        f = createModelledFunction(modified_func_def=lambda arg_values: arg_values[0]*10)
        self.assertTrue(f.id)
        self.assertEqual(f.evaluate(arg_values=[10]), 100)

    def test_conditional_calls(self):
        pass

    def test_analyse_func(self):
        func = sum_a_b
        #self.fail("\n"+dump((meta.decompiler.decompile_func(func)), indent='    '))

