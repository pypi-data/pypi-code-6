def list(the_list):
    for i in the_list:
        if isinstance(i,list):
            liebiao(i)
        else:
            print (i)
