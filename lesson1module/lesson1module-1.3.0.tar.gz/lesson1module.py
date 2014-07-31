


def discover_list (p_thelist, p_taboption = 2, indent = False):
        for v_item in p_thelist:
                if isinstance (v_item, list):
                        discover_list(v_item,p_taboption + 1, indent )                                                               
                else:
                        if indent:
                                # The for below is to first print tabs as requested in the p_taboption param
                                for p_tab_s in range(p_taboption):
                                        print("\t", end='')
                        print (v_item) 

