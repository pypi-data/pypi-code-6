from __future__ import absolute_import

import keyring.http

enabled = 'keyring' in globals()

base = keyring.http.PasswordMgr if enabled else object

class FixedUserKeyringPasswordManager(base):
	def __init__(self, username):
		self.username = username

	def get_username(self, realm, authuri):
		return self.username

	# provide clear_password until delete_password is officially
	#  implemented.
	def clear_password(self, realm, authuri):
		user = self.get_username(realm, authuri)
		# this call will only succeed on WinVault for now
		keyring.get_keyring().delete_password(realm, user)
