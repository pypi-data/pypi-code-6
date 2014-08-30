def sub_items (list_name,tab_space):
    for each_fun_items in list_name:
        if isinstance(each_fun_items, list):
            sub_items(each_fun_items,tab_space)
        else:
            for space in range(tab_space):
                print "\t",
            print (each_fun_items)

# print ("\nMulti Level List\n-----------------")
# movies = ["The Holy Grail",1987,91,\
#           ["Director",\
#            ["Actor1","Actor2","Actress1"\
#             ]\
#            ]\
#           ]
# sub_items(movies,2)


# OUTPUT
# ---------
# Printing through function
# ------------------
# 
# The Holy Grail
# 1987
# 91
# Director
# Actor1
# Actor2
# Actress1    
            








