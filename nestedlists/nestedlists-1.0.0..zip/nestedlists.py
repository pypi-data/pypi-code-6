"""Hello Python community! As is very obvious, this is my first module!"""

def function (names):
    """  Well, basically, what this does is takes an argument called names (any list) which may or
    may not have nested lists and recursively prints each data irrespective of number of deeper lists,
    one on each line."""

    for each_name in names:
	    if isinstance (each_name,list ):
		    function(each_name)
	    else:
		    print(each_name)
