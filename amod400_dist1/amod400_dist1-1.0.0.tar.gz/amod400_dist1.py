def sub_items (list_name):
    for each_fun_items in list_name:
        if isinstance(each_fun_items, list):
            sub_items(each_fun_items)
        else:
            print each_fun_items

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
            








