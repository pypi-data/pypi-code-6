#def fixtures_wrapper(app_name):
#
#  def fixtures(module, yaml_file):
#
#    yaml_file = Path.cwd().child(app_name, module, 'tests', 'fixtures', '%s.yml' % yaml_file)
#
#    with open(yaml_file) as yaml_file:
#      fixtures = yaml.load(yaml_file.read())
#
#    def load_fixture(fixture_name):
#      if fixture_name in fixtures:
#        return fixtures[fixture_name]
#      else:
#        raise LookupError('%s doesnt exists in this fixture file' % fixture_name)
#
#    return load_fixture
#  return fixtures

import os
import yaml

def fixture(module):
  current_path = os.getcwd()
  fixture_path = "%s/tests/fixtures/%s.yml" % (current_path, module)

  with open(fixture_path) as fixture_file:
    yaml_fixture = yaml.load(fixture_file.read())

  def load_fixture(fixture_key):
    if fixture_key in yaml_fixture:
      return yaml_fixture[fixture_key]
    else:
      raise LookupError("Could not find key %s in file %s" % \
                       (fixture_key, fixture_path))

  return load_fixture
