# coding=utf8

"""
Bell
~~~~
Realtime anomalies detection based on statsd, for periodic time series.
"""

#  [statsd]
#     |
#     v        send to queue
# [listener] -----------------> [beanstalkd]
#                                   |
#                                   | reserve
#             history metrics       v       record anomalies
#             ---------------> [analyzers] ----------------
#             |                     |                     |
#             |                     | put to ssdb         |
#             |                     v                     |
#             ------------------- [ssdb] <-----------------
#                                   |
#                                   |
#                                   v
#                                [webapp]


__version__ = '0.5.6'
__copyright__ = 'Eleme Inc.'
