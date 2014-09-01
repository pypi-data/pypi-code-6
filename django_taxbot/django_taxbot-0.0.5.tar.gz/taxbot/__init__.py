__version__ = '0.0.4'
__author__ = 'Seiyifa Tawari'
__license__ = 'BSD'
__copyright__ = 'Copyright 2014 Seiyifa Tawari'

import logging, decimal
from exceptions import KeyError

from taxbot import taxes as taxzz
from taxbot.models import Tax, CanadianTax

def round_decimal(interest):
	# Ensures that decimals are always
	# rounded to two places.
	TWO_PLACES = decimal.Decimal(10) ** -2
	output = decimal.Decimal(str(interest)).quantize(TWO_PLACES)

	return output

class TaxKeyError(KeyError):
	""" 
	Error to be thrown when someone requests a key we do not know about 

	"""
	def __init__(self, message=''):
		self.message = message

	def __unicode__(self):
		return self.message

	def __str__(self):
		return self.__unicode__()

class TaxClient(object):
	# This class is used in building a new tax instance

	def __init__(self, _type='S'):
		"""
		Constructor for the :class:TaxClient.
		We only set the type of tax here. 

		:param _type:
			@type: 			String
			@description: 	The type of tax which we are interested in creating
			@options: 		`S` -> SALES
							`M` -> MEALS
		
		"""
		if _type != 'S' and _type != 'M':
			raise TaxKeyError('You have entered an invalid tax type.')

		self.type = _type
		self.taxes = taxzz.TAXES
		self.currencies = taxzz.CURRENCY_DICT
		self.non_city = taxzz.NON_CITY_COUNTRIES
		self.simple_tax = taxzz.SIMPLE_TAX_COUNTRIES


	def tax_known(self, country, region=None, city=None):
		"""
		Checks that the app is aware of the tax for the
		location in question

		:param country:
			@type: 			String
			@description: 	Country in ISO Code-2 format
			@options: 		See http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
							Please refer to README for all covered countries

		:param region:
			@type: 			String
			@description: 	Also 2 letter codes for US States and Canadian Provinces

		:param
		
		"""
		if country:
			country = country.upper()
		if region:
			region = region.upper()
		if city:
			city = city.upper()

		if not country in self.taxes:
			return False
		
		if country in self.simple_tax:
			return True

		if not region:
			if not country in self.simple_tax and country in self.taxes:
				raise TaxKeyError('Invalid parameter entry. Try adding a region')

		if region and country and not city:
			try:
				region = self.taxes[country][region]
				
			except KeyError:
				raise TaxKeyError('We do not have a tax entry for this region at this time. Please follow the project closely for updates.')

			if country not in self.non_city:
				return False

			return True

		if region and country and city:
			if country in self.non_city:
				try:
					region = self.taxes[country][region]
				except KeyError:
					raise TaxKeyError('We do not have a tax entry for this region at this time. Please follow the project closely for updates.')
			else:
				try:
					city = self.taxes[country][region][city]

				except KeyError:
					raise TaxKeyError('We do not have a tax entry for this city at this time. Please follow the project closely for updates.')
				return True

		return False

	def get_tax(self, country, region=None, city=None):
		"""
		Returns the tax if it is known. Bear in mind that the returned 
		Tax may be a dictionary or a single decimal value, so please 
		perform your own checks to sanitize the input.

		Parameters are same as above

		"""
		if country:
			country = country.upper()
		if region:
			region = region.upper()
			if country in self.simple_tax:
				region = None
		if city:
			city = city.upper()
			if country in self.non_city:
				city = None

		if self.type == 'S':
			scope = 'SALES'
		else:
			scope = 'MEALS'

		try:
			self.tax_known(country, region, city)
		except KeyError:
			raise TaxKeyError('We do not currently have the requested tax rate for that location. Please watch the project closely for updates')

		if region and city:
			return self.taxes[country][region][city][scope]
		elif region and not city:
			return self.taxes[country][region][scope]
		elif country and not region and not city:
			return self.taxes[country][scope]


	def calculate_tax(self, amount, country, region=None, city=None):
		"""
		Calculates the tax and returns the total tax. 

		Note that this method ALWAYS return a dictionary. The dictionary
		comprises the followring keys:

			@mandatory: 	total -> contains the total calculated tax
			@conditional: 	GST, HST, PST (For Canadian queries)

		"""
		try:
			tax_rate = self.get_tax(country, region, city)
		except KeyError:
			raise TaxKeyError('An error occured while determining the tax rate. Please verify the rate exists by calling on the `tax_known` method.')

		return_dict = {}

		if isinstance(tax_rate, decimal.Decimal):
			amount = round_decimal(amount * tax_rate)
			return_dict['total'] = amount
			return return_dict

		else:
			total = decimal.Decimal('0.00')
			for rate in tax_rate:
				if tax_rate[rate] is not None:
					amount = round_decimal(amount * tax_rate[rate])
					return_dict[rate] = amount
					total += amount

			return_dict['total'] = total
			return return_dict

	def create_tax(self, amount, country, region=None, city=None):
		"""
		Creates a :class:Tax (and :class:CanadianTax) object for the 
		calculated tax.

		"""
		try:
			tax = self.calculate_tax(amount, country, region, city)
		except KeyError:
			raise TaxKeyError('Unable to create tax object. Please confirm all your parameters by calling the `tax_known` method.')

		try:
			currency = self.currencies[country.upper()]
			tax_object = Tax.objects.create(amount=tax['total'], currency=currency)

		except KeyError:
			raise TaxKeyError('We have no currency for that country.')

		if 'GST' in tax or 'HST' in tax or 'PST' in tax:
			# This is a CanadianTax
			can_tax = CanadianTax.objects.create(base=tax_object)
			if 'GST' in tax:
				can_tax.gst = tax['GST']
			if 'HST' in tax:
				can_tax.hst = tax['HST']
			if 'PST' in tax:
				can_tax.pst = tax['PST']

			can_tax.save()

		return tax_object
