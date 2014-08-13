"""This is to test the Version 1 """
def list_scan (the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            list_scan(each_item,level)
        else:
            for count in range(level):
                print(each_item)
            
                
                
            
