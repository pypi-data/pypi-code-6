# Copyright (C) 2010, 2011 Linaro Limited
#
# Author: Zygmunt Krynicki <zygmunt.krynicki@linaro.org>
#
# This file is part of django-testscenarios.
#
# django-testscenarios is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation
#
# django-testscenarios is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-testscenarios.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import django

from django.db import models, transaction
from django.test import (
    TestCase as DjangoTestCase,
    TransactionTestCase as DjangoTransactionTestCase)

from django_testscenarios.ubertest import (
    TestCase,
    TestCaseWithScenarios,
    TransactionTestCase,
    TransactionTestCaseWithScenarios)


if hasattr(django, 'setup'):
    django.setup()


class TestModel(models.Model):
    """
    Model for testing database configuration/initialization
    """
    field = models.CharField(max_length=10, null=True)


class ScenarioParametersAreVisibleChecks(object):

    scenarios = [
        ('scenario_a', {'attr': 'foo'}),
        ('scenario_b', {'attr': 'bar'}),
    ]

    def test_attr_is_set(self):
        self.assertNotEqual(getattr(self, 'attr'), None)


class PlainDatabaseChecks(object):

    def _do_check_for_database_state(self):
        self.assertEqual(TestModel.objects.all().count(), 0)
        obj = TestModel.objects.create()
        self.assertEqual(TestModel.objects.all().count(), 1)

    def test_database_is_empty_at_start_of_test_first(self):
        self._do_check_for_database_state()

    def test_database_is_empty_at_start_of_test_second(self):
        self._do_check_for_database_state()


class TransactionChecks(object):

    def _create_object(self):
        self.obj = TestModel.objects.create(field=None)
        self.pk = self.obj.pk

    def _reload_object(self):
        self.obj = TestModel.objects.get(pk=self.pk)

    def _commit_and_reload(self):
        transaction.commit()
        self._reload_object()

    def _rollback_and_reload(self):
        transaction.rollback()
        self._reload_object()

    def test_transaction_handling(self):
        transaction.enter_transaction_management()
        transaction.managed(True)
        try:
            self._create_object()
            self._commit_and_reload()
            self.assertEqual(self.obj.field, None)
            self.obj.field = "something"
            self.obj.save()
            self._rollback_and_reload()
            self.assertEqual(self.obj.field, None)
        finally:
            transaction.rollback()
            transaction.leave_transaction_management()


# Non-transaction tests


class TestsWorkWithPlainDjangoTestCase(DjangoTestCase,
                                       PlainDatabaseChecks):
    """
    Test class that is using:
        * plain database checks
        * django test case
    """


class TestsWorkWithTestToolsTestCase(TestCase,
                                     PlainDatabaseChecks):
    """
    Test class that is using:
        * plain database checks
        * test tools test case
    """


class TestsWorkWithTestScenariosTestCaseAndNoScenarios(TestCaseWithScenarios,
                                                       PlainDatabaseChecks):
    """
    Test class that is using:
        * plain database checks
        * test tools test case
        * test scenarios test case
        * no actual scenarios (short-circuited fast path)
    """


class TestsWorkWithTestScenariosTestCaseAndSomeScenarios(TestCaseWithScenarios,
                                                         ScenarioParametersAreVisibleChecks,
                                                         PlainDatabaseChecks):
    """
    Test class that is using:
        * database transactions
        * test tools test case
        * test scenarios test case
        * two dummy scenarios so that multiple test cases get generated
    """


# Transaction tests


class TransactionsWorkWithPlainDjangoTestCase(DjangoTransactionTestCase,
                                              PlainDatabaseChecks,
                                              TransactionChecks):
    """
    Test class that is using:
        * database transactions
        * django test case (with transaction support)
    """


class TransactionsWorkWithTestToolsTestCase(TransactionTestCase,
                                            PlainDatabaseChecks,
                                            TransactionChecks):
    """
    Test class that is using:
        * database transactions
        * test tools test case (with transaction support)
    """


class TransactionsWorkWithTestScenariosTestCaseAndNoScenarios(TransactionTestCaseWithScenarios,
                                                              PlainDatabaseChecks,
                                                              TransactionChecks):
    """
    Test class that is using:
        * database transactions
        * test tools test case (with transaction support)
        * test scenarios test case (with transaction support)
        * no actual scenarios (short-circuited fast path)
    """


class TransactionsWorkWithTestScenariosTestCaseAndSomeScenarios(TransactionTestCaseWithScenarios,
                                                                ScenarioParametersAreVisibleChecks,
                                                                PlainDatabaseChecks,
                                                                TransactionChecks):
    """
    Test class that is using:
        * database transactions
        * test tools test case (with transaction support)
        * test scenarios test case (with transaction support)
        * two dummy scenarios so that multiple test cases get generated
    """


class TestReorderingNotBroken(DjangoTestCase):
    """
    Test that test suite reordering done inside DjangoTestSuiteRunner
    class (to optimize database setup/tear down code) is not going to
    reorder our improved test classes.
    """

    class Plain(TestCase):
        """" Empty test class inheriting from TestCase """

        def runTest(self, result):
            pass

    class PlainScenarios(TestCaseWithScenarios):

        def runTest(self, result):
            pass

    class Transaction(TransactionTestCase):
        """" Empty test class inheriting from TransactionTestCase """

        def runTest(self, result):
            pass

    class TransactionScenarios(TransactionTestCaseWithScenarios):
        """" Empty test class inheriting from TransactionTestCase """

        def runTest(self, result):
            pass

    def ensure_proper_order(self, initial_order, proper_order):
        """
        Create a TestSuite with test cases in initial_order, reorder
        them using the same logic that Django applies and verify that
        the order is proper_order
        """
        from django.test.runner import reorder_suite

        suite = unittest.TestSuite()
        for cls in initial_order:
            suite.addTest(cls())
        reordered_suite = reorder_suite(suite, (DjangoTestCase,))
        self.assertEqual(map(type, reordered_suite._tests), proper_order)

    def test_transaction_test_case_stays_last(self):
        self.ensure_proper_order(
            [self.Plain, self.Transaction],
            [self.Plain, self.Transaction])

    def test_transaction_test_case_is_moved_to_be_last(self):
        self.ensure_proper_order(
            [self.Transaction, self.Plain],
            [self.Plain, self.Transaction])

    def test_transaction_scenarios_test_case_stays_last(self):
        self.ensure_proper_order(
            [self.Plain, self.TransactionScenarios],
            [self.Plain, self.TransactionScenarios])

    def test_transaction_scenarios_test_case_is_moved_to_be_last(self):
        self.ensure_proper_order(
            [self.TransactionScenarios, self.Plain],
            [self.Plain, self.TransactionScenarios])

    def test_plain_test_case_stays_first(self):
        self.ensure_proper_order(
            [self.Plain, self.Transaction],
            [self.Plain, self.Transaction])

    def test_plain_test_case_is_moved_to_be_first(self):
        self.ensure_proper_order(
            [self.Transaction, self.Plain],
            [self.Plain, self.Transaction])

    def test_plain_test_case_stays_first(self):
        self.ensure_proper_order(
            [self.Plain, self.Transaction],
            [self.Plain, self.Transaction])

    def test_plain_scenarios_test_case_is_moved_to_be_first(self):
        self.ensure_proper_order(
            [self.Transaction, self.PlainScenarios],
            [self.PlainScenarios, self.Transaction])

    def test_plain_scenarios_test_case_stays_first(self):
        self.ensure_proper_order(
            [self.PlainScenarios, self.Transaction],
            [self.PlainScenarios, self.Transaction])
