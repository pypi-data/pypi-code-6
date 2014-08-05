#!/usr/bin/python
import bootd
import sys
import os


bootd_path = os.path.dirname(bootd.__file__)
template_path = os.path.join(bootd_path, 'project_template')

sys.argv.append('--template={}'.format(template_path))
sys.argv.append('--extension=py,html')

from django.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
