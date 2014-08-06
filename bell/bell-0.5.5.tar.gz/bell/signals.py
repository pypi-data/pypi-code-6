# coding=utf8


from blinker import signal


datapoint_reserved = signal('datapoint_reserved')
anomaly_detected = signal('anomaly_detected')
analyzation_done = signal('analyzation_done')
