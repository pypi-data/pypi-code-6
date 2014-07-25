"""Here I've defined a function namely print_r which will help you work on
a list data which is nested inside a nested list which is nested inside a
nested list and so on.And something more about this is that it'll also help
you to figure out the indentation of the list data in case you want it to do
so."""
def print_r(the_list,indent=False,level=0):
    """If you want the indentation facility you need to specify while
calling the function e.g.-print_r(list_name,True,2):this type of function
call will print the list items and will provide the indentation with two tab
stops each nested items"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_r(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='')
            print(each_item)    
