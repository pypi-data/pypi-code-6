import os

class LoadAverage:
    """ Returns the load average over the last 1, 5 and 15 minutes """

    def getVariableTuple(self):

        load_avg = os.getloadavg()

        return [
            ('LOAD_AVG_1', load_avg[0]),
            ('LOAD_AVG_5', load_avg[1]),
            ('LOAD_AVG_15', load_avg[2])
        ]