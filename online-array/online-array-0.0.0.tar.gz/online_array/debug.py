#!/usr/bin/env python

import online_array

array = online_array.OnlineArray((5, ), function=lambda x: x + 1)

for i in array:
    print i
