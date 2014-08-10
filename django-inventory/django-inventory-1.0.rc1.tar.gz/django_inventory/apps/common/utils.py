def encapsulate(function):
    # Workaround Django ticket 15791
    # Changeset 16045
    # http://stackoverflow.com/questions/6861601/cannot-resolve-callable-context-variable/6955045#6955045
    return lambda: function
