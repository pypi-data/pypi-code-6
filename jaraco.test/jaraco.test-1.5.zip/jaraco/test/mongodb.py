import pytest
try:
	import pymongo
except ImportError:
	pass

from . import services

@pytest.yield_fixture(scope='session')
def mongodb_instance():
	try:
		instance = services.MongoDBInstance()
		instance.log_root = ''
		instance.start()
		pymongo.Connection(instance.get_connect_hosts())
		yield instance
	except Exception:
		pytest.skip("MongoDB not available")
	instance.stop()

@pytest.fixture(scope='session')
def mongodb_uri(mongodb_instance):
	return mongodb_instance.get_uri()
