import re

def check(raw_data, tld_addr):	
	if tld_addr == "whois.aero":
		return aero_check(raw_data)
	elif tld_addr == "whois.iana.org":
		return arpa_check(raw_data)
	elif tld_addr == "whois.nic.asia":
		return asia_check(raw_data)
	elif tld_addr == "whois.biz":
		return biz_check(raw_data)
	elif tld_addr == "whois.cat":
		return cat_check(raw_data)
	elif tld_addr == "whois.verisign-grs.com":
		return com_check(raw_data)
	else:
		return -1
	
	return -1
	if self._error_check == 1:
		self._display_fail("Failed to get WHOIS DATA")
		return -1
	
	regex = re.compile("No match for \"%s\"\." % self._domain.upper())
	match = regex.search(self._raw_socket)
	if match:
		self._display_safe("Yes can Get")
		return 1
	
	self._display_fail("No can Get")
	return 0

def aero_check(raw_data):
	return regex_support(raw_data, "Access ")

def arpa_check(raw_data):
	return regex_support(raw_data, "% This query returned 1 objects.")

def asia_check(raw_data):
	return regex_support(raw_data, "DotAsia ")

def biz_check(raw_data):
	return regex_support(raw_data, "Domain ")

def cat_check(raw_data):
	return regex_support(raw_data, "Domain ID:")

def com_check(raw_data):
	return ~regex_support(raw_data, "No match for") + 2

def regex_support(raw_data, regex_word):
	regex = re.compile(regex_word)
	match = regex.search(raw_data)
	
	if match:
		return 0
	return 1
