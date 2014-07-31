

def discover_list (p_thelist, p_taboption=0):
        for v_item in p_thelist:
                if isinstance (v_item, list):
                        discover_list_with_tab(v_item,p_taboption)
                else:
                        for p_tab_s in range(p_taboption):
                                print("\t", end='')
                        print (v_item)
