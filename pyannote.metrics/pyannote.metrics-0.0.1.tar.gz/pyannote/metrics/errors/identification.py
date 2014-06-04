#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2012-2014 CNRS (Hervé BREDIN - http://herve.niderb.fr)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals

import numpy as np
from munkres import Munkres

from ..matcher import LabelMatcherWithUnknownSupport
from pyannote.core import Annotation
from pyannote.core.matrix import LabelMatrix
from pyannote.algorithms.tagging import DirectTagger

from ..matcher import MATCH_CORRECT, MATCH_CONFUSION, \
    MATCH_MISSED_DETECTION, MATCH_FALSE_ALARM

REGRESSION = 'regression'
IMPROVEMENT = 'improvement'
BOTH_CORRECT = 'both_correct'
BOTH_INCORRECT = 'both_incorrect'


class IdentificationErrorAnalysis(object):

    def __init__(self, matcher=None, unknown=True):

        super(IdentificationErrorAnalysis, self).__init__()

        if matcher is None:
            matcher = LabelMatcherWithUnknownSupport()
        self.matcher = matcher

        self.unknown = unknown
        self._munkres = Munkres()
        self._tagger = DirectTagger()

    def __call__(self, reference, hypothesis):
        """

        Returns
        -------
        diff : `Annotation`
            Annotation containing list of errors ()

        """

        # common (up-sampled) timeline
        common_timeline = reference.get_timeline().union(
            hypothesis.get_timeline())
        common_timeline = common_timeline.segmentation()

        # align reference on common timeline
        R = self._tagger(reference, common_timeline)

        # translate and align hypothesis on common timeline
        H = self._tagger(hypothesis, common_timeline)

        errors = Annotation(uri=reference.uri, modality=reference.modality)

        # loop on all segments
        for segment in common_timeline:

            # list of labels in reference segment
            rlabels = R.get_labels(segment, unknown=self.unknown, unique=False)

            # list of labels in hypothesis segment
            hlabels = H.get_labels(segment, unknown=self.unknown, unique=False)

            _, details = self.matcher(rlabels, hlabels)

            for r, h in details[MATCH_CORRECT]:
                track = errors.new_track(segment, prefix=MATCH_CORRECT)
                errors[segment, track] = (MATCH_CORRECT, r, h)

            for r, h in details[MATCH_CONFUSION]:
                track = errors.new_track(segment, prefix=MATCH_CONFUSION)
                errors[segment, track] = (MATCH_CONFUSION, r, h)

            for r in details[MATCH_MISSED_DETECTION]:
                track = errors.new_track(segment, prefix=MATCH_MISSED_DETECTION)
                errors[segment, track] = (MATCH_MISSED_DETECTION, r, None)

            for h in details[MATCH_FALSE_ALARM]:
                track = errors.new_track(segment, prefix=MATCH_FALSE_ALARM)
                errors[segment, track] = (MATCH_FALSE_ALARM, None, h)

        return errors

    def confusion_matrix(self, reference, hypothesis):

        rlabels = sorted(reference.labels(unknown=self.unknown) + [None])
        hlabels = sorted(hypothesis.labels(unknown=self.unknown) + [None])
        data = np.zeros((len(rlabels), len(hlabels)))
        matrix = LabelMatrix(data=data, rows=rlabels, columns=hlabels)

        chart = self(reference, hypothesis).chart()
        for (error, rlabel, hlabel), duration in chart:
            matrix[rlabel, hlabel] = duration

        return matrix

    def _match_errors(self, old_error, new_error):
        old_type, old_ref, old_hyp = old_error
        new_type, new_ref, new_hyp = new_error
        return (old_ref == new_ref) * ((old_type == new_type) + (old_hyp == new_hyp))

    def regression(self, reference, old_hypothesis, new_hypothesis):

        reference = reference.smooth()
        old_hypothesis = old_hypothesis.smooth()
        new_hypothesis = new_hypothesis.smooth()

        old_diff = self(reference, old_hypothesis, correct=True).smooth()
        new_diff = self(reference, new_hypothesis, correct=True).smooth()

        common_timeline = old_diff.get_timeline().union(new_diff.get_timeline())
        common_timeline = common_timeline.segmentation()
        old_diff = old_diff >> common_timeline
        new_diff = new_diff >> common_timeline

        regression = Annotation(uri=reference.uri, modality=reference.modality)

        for segment in common_timeline:

            old_errors = old_diff.get_labels(segment, unique=False)
            new_errors = new_diff.get_labels(segment, unique=False)

            n1 = len(old_errors)
            n2 = len(new_errors)
            n = max(n1, n2)

            match = np.zeros((n, n), dtype=int)
            for i1, e1 in enumerate(old_errors):
                for i2, e2 in enumerate(new_errors):
                    match[i1, i2] = self._match_errors(e1, e2)

            mapping = self._munkres.compute(2 - match)

            for i1, i2 in mapping:

                if i1 >= n1:
                    track = regression.new_track(segment, prefix=REGRESSION)
                    regression[segment, track] = (REGRESSION, None, new_errors[i2])

                elif i2 >= n2:
                    track = regression.new_track(segment, prefix=IMPROVEMENT)
                    regression[segment, track] = (IMPROVEMENT, old_errors[i1], None)

                elif old_errors[i1][0] == MATCH_CORRECT:

                    if new_errors[i2][0] == MATCH_CORRECT:
                        track = regression.new_track(segment, prefix=BOTH_CORRECT)
                        regression[segment, track] = (BOTH_CORRECT, old_errors[i1], new_errors[i2])

                    else:
                        track = regression.new_track(segment, prefix=REGRESSION)
                        regression[segment, track] = (REGRESSION, old_errors[i1], new_errors[i2])

                else:

                    if new_errors[i2][0] == MATCH_CORRECT:
                        track = regression.new_track(segment, prefix=IMPROVEMENT)
                        regression[segment, track] = (IMPROVEMENT, old_errors[i1], new_errors[i2])

                    else:
                        track = regression.new_track(segment, prefix=BOTH_INCORRECT)
                        regression[segment, track] = (BOTH_INCORRECT, old_errors[i1], new_errors[i2])

        return regression.smooth()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
