#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
import sys
import codecs

RUN_SCRIPT = """
#!/bin/bash

{env}

python {file}
exit $?
"""

INIT_ENV = os.environ["__PY_T_SUBMIT_ENV"]

ROOT_DIR = os.environ["__PY_T_SUBMIT_DIRNAME"]
EXECUTOR = os.path.join(ROOT_DIR, 'torque_executor.py')

init_file = tempfile.NamedTemporaryFile(suffix=".sh", delete=False,)

with codecs.open(init_file.name, 'w', encoding='utf-8') as f:
    f.write(RUN_SCRIPT.format(env=INIT_ENV, file=EXECUTOR))

sys.exit(os.system("bash " + init_file.name))