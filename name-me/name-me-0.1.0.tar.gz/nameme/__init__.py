import os
import random


__version__ = '0.1.0'
__author__ = 'Kasper Jacobsen'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Kasper Jacobsen'


class MissingParameterException(Exception):
	pass

class NameMe:
	def __init__(self, adjectives=None, nouns=None, seperator=' '):
		self.adjectives = adjectives
		self.nouns = nouns
		self.seperator = seperator
		self.adjective_index = self._get_index(adjectives)
		self.noun_index = self._get_index(nouns)
		
		self.first_part = self.adjectives[self.adjective_index]
		self.last_part = self.nouns[self.noun_index]

		self.name = self.get_name()

	@staticmethod
	def _get_index(iterable):
		if iterable:
			return random.randrange(len(iterable))
		raise MissingParameterException("Missing parameter")

	@staticmethod
	def _regenerate_word(iterable, old_index, old_word, retries=5):
		new_index = random.randrange(len(iterable))
		for i in xrange(retries):
			if new_index != old_index:
				break
		return iterable[new_index], random.randrange(len(iterable))

	def regenerate_adjective(self):
		self.first_part, self.adjective_index = self._regenerate_word(
			self.adjectives,
			self.adjective_index,
			self.first_part
		)
		self.name = self.get_name()

	def regenerate_noun(self):
		self.last_part, self.noun_index = self._regenerate_word(
			self.nouns,
			self.noun_index,
			self.last_part
		)
		self.name = self.get_name()

	def get_name(self):
		return self.first_part + self.seperator + self.last_part
