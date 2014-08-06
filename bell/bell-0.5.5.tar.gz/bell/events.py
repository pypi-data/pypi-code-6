# coding=utf8

from bell.signals import anomaly_detected, analyzation_done, datapoint_reserved


def on_datapoint_reserved(hook):
    datapoint_reserved.connect(hook)
    return hook


def on_anomaly_detected(hook):
    anomaly_detected.connect(hook)
    return hook


def on_analyzation_done(hook):
    analyzation_done.connect(hook)
    return hook
