import sys

def print_lol(the_list,fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
            print("came here as list")
            print_lol(each_item,fh)
        else:
            try:
                print("came here")
                fh.write(each_item)
            except IOError:
                print("File error")
                
    fh.close();
    
    
        
    
