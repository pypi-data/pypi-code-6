#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'


def test_import_of_all_modules():
    from transmedia import conversion
    from transmedia import encoders
    from transmedia import io
    from transmedia import util
    from transmedia import transform_png
