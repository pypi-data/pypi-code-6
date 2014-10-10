from unittest import TestCase

from vecnet.simulation import submission_status


class SubmissionStatusTests(TestCase):
    """
    Tests of the submission_status module.
    """

    def test_max_length(self):
        """
        Test to ensure all known IDs are within the MAX_LENGTH.
        """
        for status in submission_status.ALL:
            self.assertLessEqual(len(status), submission_status.MAX_LENGTH)
