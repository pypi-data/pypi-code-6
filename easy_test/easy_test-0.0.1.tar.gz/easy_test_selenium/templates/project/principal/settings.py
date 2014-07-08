"""
Easy Test Selenium settings for this project test.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Web Driver definition
WEB_DRIVERS = (
    {'browser':'firefox',
     'path':'/usr/bin/firefox/firefox'},
)

IMPLICITLY_WAIT = 30

# URL to be tested
URL_BASE = 'http://frontend-labs.com/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Test Cases definition
TEST_APPS = [

]

