#!/usr/bin/python
import bootd
import subprocess
import sys
import os


path = os.path.dirname(bootd.__file__)
# print path
# print sys.argv

if __name__ == "__main__":
    subprocess.call(["django-admin.py", "startproject", "testsub", path])
