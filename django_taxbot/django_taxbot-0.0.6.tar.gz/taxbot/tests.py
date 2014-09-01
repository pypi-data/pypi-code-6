import decimal
from django.test import TestCase
from taxbot import TaxClient
from taxbot.models import Tax, CanadianTax

from django.core.exceptions import ObjectDoesNotExist

# Create your tests here.
class TaxClientTests(TestCase):
	# Tests the :class:TaxClient

	def setUp(self):
		self.client = TaxClient()

	def tearDown(self):
		del self.client

	def test_initialize(self):
		# Assert that the :class:TaxClient is 
		# created properly
		client = TaxClient()
		self.assertEqual(client.type, 'S')

		client = TaxClient('M')
		self.assertEqual(client.type, 'M')

	def test_tax_known(self):
		# Assert that the :class:TaxClient
		# reports on only known tax rates
		self.assertTrue(self.client.tax_known('ca', 'bc'))
		self.assertFalse(self.client.tax_known('ca', 'bc', 'brisco'))

		self.assertTrue(self.client.tax_known('gb', 'bc'))
		self.assertFalse(self.client.tax_known('nl'))

		self.assertRaises(KeyError, lambda: self.client.tax_known('ca', 'az', 'phoenix'))

	def test_get_tax(self):
		# Assert that the :class:TaxClient
		# reports the correct tax as saved internally
		self.assertIsInstance(self.client.get_tax('gb'), decimal.Decimal)
		self.assertIsInstance(self.client.get_tax('ca', 'bc'), dict)

	def test_calculate_tax(self):
		# Assert that a dictionary is returned
		amount = decimal.Decimal('15.00')
		total = self.client.calculate_tax(amount, 'gb')
		self.assertIsInstance(total, dict)
		self.assertTrue('total' in total)

		total = self.client.calculate_tax(amount, 'ca', 'bc')
		self.assertIsInstance(total, dict)
		self.assertTrue('total' in total)

		total = self.client.calculate_tax(amount, 'us', 'az', 'phoenix')
		self.assertIsInstance(total, dict)
		self.assertTrue('total' in total)

	def test_create_tax(self):
		# Assert that the :class:Tax object is created
		amount = decimal.Decimal('15.00')
		tax = self.client.create_tax(amount, 'gb')
		self.assertIsInstance(tax, Tax)
		self.assertRaises(ObjectDoesNotExist, lambda: tax.ca_tax)

		tax = self.client.create_tax(amount, 'ca', 'bc')
		self.assertIsInstance(tax, Tax)
		self.assert_(tax.ca_tax)
