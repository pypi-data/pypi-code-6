from unittest import TestCase

from vecnet.simulation import sim_status


class SimStatusTests(TestCase):
    """
    Tests of the sim_status module.
    """

    def test_max_length(self):
        """
        Test to ensure all known IDs are within the MAX_LENGTH.
        """
        for status in sim_status.ALL:
            self.assertLessEqual(len(status), sim_status.MAX_LENGTH)
