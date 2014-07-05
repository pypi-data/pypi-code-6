import os 
import pkg_resources
from util import parse_task_tree


DEFAULT_TASK_PATH = os.path.dirname(
  pkg_resources.resource_filename('gnulynx', 'tasks/__init__.py')
 )


DEFAULT_TREE = parse_task_tree(DEFAULT_TASK_PATH)

