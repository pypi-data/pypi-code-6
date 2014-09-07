"""
Use Case 2: User Movie Preferences to Determine User Similarity Network

Note: These simulations are for example use cases only
and are not intended to be an accurate model of any real
situation.  Do not attempt to use these for anything other
than understanding the workings of the InversionTest package.

Author: Benjamin D. Nye
License: Apache License V2.0
"""

def readPreferencesFile(fileName, rowSep='\n', colSep=',', gradeSep=';'):
    """
    Read the preference lists from a CSV-formatted file.
    A file with the data:
    "Person1,MovieA,MovieB,...,MovieN\nPerson2,MovieB,MovieA,MovieC,..."
    Corresponding to the preference ordering of Person1, Person2, etc
    for the list of movies given.
    @param fileName: Name of the input file to read the simulation results
    @type fileName: str
    @param rowSep: Separator for rows.  For CSV, should be '\n' or '\r'
    @type rowSep: str
    @param colSep: Separator for columns.  For CSV, should be ','
    @type colSep: str
    @param gradeSep: Separator for grades within a cell.
    @type gradeSep: str
    @return: Map of individuals to their movie preference ordering
    @rtype: dict of {str : list of list of str}
    """
    with open(fileName, 'r') as inFile:
        data = inFile.read()
    prefs = [(result.split(colSep)[0], [[x for x in grade.split(gradeSep)]
              for grade in result.split(colSep)[1:]]) for result in data.split(rowSep)]
    return dict(prefs)

if __name__ == '__main__':
    from InversionTest import inversionSimilarity

    # Constants
    similarityThreshold = 0.75

    # Load the file with the preference lists
    preferenceFile = 'MoviePreferences.csv'
    prefLists = readPreferencesFile(preferenceFile)

    # Calculate Similarities Between User Preferences
    userSimilarities = {}
    for user1, prefList1 in prefLists.items():
        userSimilarities[user1] = {}
        for user2, prefList2 in prefLists.items():
            similarity = inversionSimilarity(prefList1, prefList2, isGraded=True)
            # Store Edge if Similarity > Threshold
            if similarity > similarityThreshold:
                userSimilarities[user1][user2] = similarity
            
    # Use these Similarities to Draw a Graph
    # Note: Requires NetworkX and Matplotlib to generate image
    try:
        import networkx
        import matplotlib.pyplot
        canVisualize = True
    except ImportError:
        print "Could not generate graph, networkx visualization unavailable"
        canVisualize = False
    if canVisualize:
        graph = networkx.Graph()
        for user1 in userSimilarities:
            for user2, similarity in userSimilarities[user1].items():
                graph.add_edge(user1, user2, weight=similarity)
        networkx.draw(graph, font_size=12, alpha=0.5, node_size=150)
        matplotlib.pyplot.show()
