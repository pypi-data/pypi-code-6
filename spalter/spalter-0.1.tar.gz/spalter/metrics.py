from collections import OrderedDict
import numpy as np
from statsmodels.stats.power import ttest_power
from statsmodels.stats.weightstats import ttest_ind, DescrStatsW, CompareMeans


# Convenience methods

def _split(observations, control_label=None):
    if control_label is None:
        first_item = list(observations.values())[0]
        control_label = list(first_item.keys())[0]
        print('Info: No control_label given, setting it to: {}'.format(control_label))

    others = OrderedDict()
    control = OrderedDict()
    for observation_label, variants in observations.items():
        for variant_label, values in variants.items():
            if variant_label == control_label:
                control[observation_label] = values
            else:
                if not variant_label in others.keys():
                    others[variant_label] = OrderedDict()
                others[variant_label][observation_label] = values
    return control, others


def _apply(data, fn, control_label):
    control, others = _split(data, control_label=control_label)
    result = OrderedDict()
    for variant_label, observations in others.items():
        result[variant_label] = OrderedDict()
        for observation_label, values in observations.items():
            result[variant_label][observation_label] = fn(control[observation_label],
                                                          others[variant_label][observation_label])
    return result


# Metrics

def mean(data, *args, **kwargs):
    """
    Calculates the mean for each observation for every variant.
    """
    result = OrderedDict()
    for observation_label, variant_values in data.items():
        result[observation_label] = OrderedDict()
        for label, values in variant_values.items():
             result[observation_label][label] = np.mean(values)
    return result


def pvalue(data, control_label=None, *args, **kwargs):
    """
    Calculates p-value for observation in the treatment group(s)
    in respect to the control group.
    """
    def fn(control, test):
        return ttest_ind(control, test)[1]

    return _apply(data, fn, control_label)


def confidence_interval(data, control_label=None, *args, **kwargs):
    """
    Calculates the confidence interval for each observation in the
    treatment group(s). Return value is tuple (low, high).
    """
    def fn(control, test):
        c_means = CompareMeans(DescrStatsW(test), DescrStatsW(control))
        return c_means.tconfint_diff()

    return _apply(data, fn, control_label)


def power(data, control_label=None, *args, **kwargs):
    """
    Calculates the statistical power for each observation in the
    treatment group(s).
    """
    def fn(control, test):
        if len(control) != len(test):
            print('Warning: sample sizes differ.')
        effect_size = _effect_size(control, test)
        return ttest_power(effect_size=effect_size,
                           nobs=len(control),
                           alpha=0.05)

    return _apply(data, fn, control_label)


def _effect_size(control, test):
    d_control = DescrStatsW(control)
    d_test = DescrStatsW(test)
    return abs((d_control.mean - d_test.mean) / d_control.std)


metrics = {
    'mean':    mean,
    'pvalue':  pvalue,
    'confint': confidence_interval,
    'power':   power
}
