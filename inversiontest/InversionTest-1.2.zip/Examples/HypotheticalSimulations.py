"""
Hypothetical Simulations of Synthetic Cannabinoid Spread

Warning: These simulations are for example use cases only
and are not intended to be an accurate model of any real
situation.  Do not attempt to use these for anything other
than understanding the workings of the InversionTest package.

Author: Benjamin D. Nye
License: Apache License V2.0
"""
from random import random

# Assumed Resistance of Each Community
# Range: -2 (very low resistance) to 2 (very high resistance)
RESISTANCE_LEVELS =    {'AU':-1.0,
                        'AV': 2.0,
                        'AW': 1.0,
                        'AX': 2.0,
                        'AY': 2.0,
                        'AZ': 2.0,
                        'BU': 2.0,
                        'BV': 2.0,
                        'BW': 0.0,
                        'BX': -1.5,
                        'BY': 0.0,
                        'BZ': 0.0,
                        'CU': 0.0,
                        'CV': 1.0,
                        'CW': 0.0,
                        'CX': 1.0,
                        'CY': 0.0,
                        'CZ': 1.0,
                        'DU': 0.2,
                        'DV': 0.3,
                        'DW': 0.5,
                        'DX': 0.1,
                        'DY': -1.2,
                        'DZ': 0.0,
                        'EU': 1.1,
                        'EV': 1.2,
                        'EW': 1.3,
                        'EX': -0.2,
                        'EY': 0.2,
                        'EZ': 0.3,
                        }

def isNeighbor(a, b):
    """
    Using string grid coordinates, check if a region is a neighbor
    @param a: Name of the first region, in the form 'XY' coordinates
    @type a: str
    @param b: Name of the second region, in the form 'XY' coordinates
    @type b:
    """
    row, col = a[0], a[1]
    row2, col2 = b[0], b[1]
    return (chr(ord(row2)+1)==row or chr(ord(row2)-1)==row or
            chr(ord(col2)+1)==col or chr(ord(col2)-1)==col)

def localizedSimulation(resistances=RESISTANCE_LEVELS, weeks=24):
    """
    Very simple local-spread simulation
    Assumes introduction to new areas due to prior susceptibility
    and due to neighboring regions adopting
    @param resistances: Mapping of region names to resistance levels
    @type resistances: dict of {str : float}
    @param weeks: Number of weeks to simulate
    @type weeks: int
    @return: Order that regions adopted, as a graded sequence
    @rtype: list of list of str
    """
    ordering = []
    allAdopters = set()
    for week in xrange(weeks):
        adopters = []
        for region, resistance in resistances.items():
            localInfluence = min(1.0, sum([1 for x in allAdopters if isNeighbor(region, x)])/4.0)
            vulnVal = max(localInfluence, (1-resistance))
            regionVal = vulnVal - random()
            if region not in allAdopters:
                adopters.append((regionVal, region))
        if adopters:
            adopter = max(adopters)[1]
            ordering.append([adopter])
            allAdopters.add(adopter)
    holdouts = [region for region in resistances if region not in allAdopters]
    if holdouts:
        ordering.append(holdouts)
    return ordering
        
def mediaSimulation(resistances=RESISTANCE_LEVELS, weeks=24):
    """
    Very simple global-spread simulation
    Assumes introduction to new areas due to prior susceptibility
    @param resistances: Mapping of region names to resistance levels
    @type resistances: dict of {str : float}
    @param weeks: Number of weeks to simulate
    @type weeks: int
    @return: Order that regions adopted, as a graded sequence
    @rtype: list of list of str
    """
    ordering = []
    allAdopters = set()
    for week in xrange(weeks):
        adopters = []
        for region, resistance in resistances.items():
            vulnVal = (1-resistance)
            regionVal = vulnVal - random()
            if region not in allAdopters:
                adopters.append((regionVal, region))
        if adopters:
            adopter = max(adopters)[1]
            ordering.append([adopter])
            allAdopters.add(adopter)
    holdouts = [region for region in resistances if region not in allAdopters]
    if holdouts:
        ordering.append(holdouts)
    return ordering



def writeSimulationResults(n, simCall, fileName, rowSep='\n', colSep=',', gradeSep=';'):
    """
    Run simulation and write the simulation results to a CSV-formatted file
    @param n: Number of simulation runs to perform
    @type n: int
    @param simCall: Function that runs a simulation and generates an ordering
    @type simCall: callable
    @param fileName: Name of the output file to write the simulation results
    @type fileName: str
    @param rowSep: Separator for rows.  For CSV, should be '\n' or '\r'
    @type rowSep: str
    @param colSep: Separator for columns.  For CSV, should be ','
    @type colSep: str
    @param gradeSep: Separator for grades within a cell.
    @type gradeSep: str
    """
    results = [simCall() for i in xrange(n)]
    outStr = rowSep.join([colSep.join([gradeSep.join(grade) for grade in result])
                          for result in results])
    with open(fileName, 'w') as outFile:
        outFile.write(outStr)

def readSimulationResults(fileName, rowSep='\n', colSep=',', gradeSep=';'):
    """
    Read the simulation results from a CSV-formatted file.
    A file with the data:
    "Element1,Element2,Element3;Element4,Element5\nElement1,Element5"
    Corresponds to the graded sequences:
    [[["Element1"], ["Element2"], ["Element3", "Element4"], ["Element5"]],
     [["Element1"], ["Element5"]]]
    @param fileName: Name of the input file to read the simulation results
    @type fileName: str
    @param rowSep: Separator for rows.  For CSV, should be '\n' or '\r'
    @type rowSep: str
    @param colSep: Separator for columns.  For CSV, should be ','
    @type colSep: str
    @param gradeSep: Separator for grades within a cell.
    @type gradeSep: str
    """
    with open(fileName, 'r') as inFile:
        data = inFile.read()
    results = [[[x for x in grade.split(gradeSep)] for grade in result.split(colSep)]
               for result in data.split(rowSep)]
    return results

if __name__ == '__main__':
    # Constants
    localSimFileName = 'LocalizedSimResults.csv'
    mediaSimFileName = 'MediaSimResults.csv'
    numRuns = 30
    # Run Simulations and Write Orderings to File
    writeSimulationResults(numRuns, localizedSimulation, localSimFileName)
    writeSimulationResults(numRuns, mediaSimulation, mediaSimFileName)
