"""This is to test the Version 1 """
def list_scan (the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            list_scan(each_item)
        else:
            print(each_item)
                
                
            
