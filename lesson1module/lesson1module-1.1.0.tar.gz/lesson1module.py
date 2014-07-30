

def discover_list_with_tab (p_thelist, p_taboption):
        for v_item in p_thelist:
                if isinstance (v_item, list):
                        discover_list_with_tab(v_item,1)
                else:
                        for p_tab_s in range(p_taboption):
                                print("\t", end='The movie is ')
                        print (v_item)
