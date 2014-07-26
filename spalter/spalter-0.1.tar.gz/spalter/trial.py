from collections import OrderedDict
from .importer import _import_csv
from .metrics import metrics as default_metrics


class Trial(object):

    """
    Represents an split test.

    Parameters
    ----------
    variant_labels : list of strings
        Labels for the groups in the trial.

    observation_labels : list of string
        Labels for the observations measured in the trial.
    """

    class UnsupportedMetricError(Exception):
        pass

    def __init__(self, variant_labels, observation_labels):
        self.observations = OrderedDict()
        for observation in observation_labels:
            variants = OrderedDict([(variant, []) for variant in variant_labels])
            self.observations[observation] = variants

    def update(self, feed):
        """
        Updates trial with new data.
        If there was data before, the new values will be appended.

        Parameters
        ----------
        feed : dict of dicts
            Contains a dict with observations as keys. The values are a dict
            with the variants as keys and the measured data as values.
        """
        for observation, variant_dict in feed.items():
            for variant, values in variant_dict.items():
                self.observations[observation][variant] = values
        return self

    def evaluate(self, metric, *args, **kwargs):
        if isinstance(metric, str):
            if metric not in default_metrics:
                raise Trial.UnsupportedMetricError(metric)
            cls = default_metrics[metric]
            result = cls(self.observations, *args, **kwargs)
        else:
            result = OrderedDict()
            for m in metric:
                if m not in default_metrics:
                    raise Trial.UnsupportedMetricError(m)
                cls = default_metrics[m]
                result[m] = cls(self.observations, *args, **kwargs)
        return result

    def read_csv(self, filename, split_column, *args, **kwargs):
        """
        Imports data from a CSV file.

        Parameters
        ----------
        filename : string
            Location of CSV file

        split_columns : string
            Name of column containing labels for test/control split.
        """
        feed = _import_csv(filename, split_column, *args, **kwargs)
        self.update(feed)
        return self
