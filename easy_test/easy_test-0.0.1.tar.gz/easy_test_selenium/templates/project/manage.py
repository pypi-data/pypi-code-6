#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("EASY_TEST_SETTINGS", "principal.settings")

    from easy_test_selenium.cmdline import execute
    execute(sys.argv)
