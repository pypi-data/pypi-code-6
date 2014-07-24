


""" This function describes how to find an item in a list and check if there is another list inside"""
def discover_list (p_thelist):
        """ My code!"""
        for v_item in p_thelist:
                if isinstance (v_item, list):
                        discover_list(v_item)
                else:
                        print (v_item)
