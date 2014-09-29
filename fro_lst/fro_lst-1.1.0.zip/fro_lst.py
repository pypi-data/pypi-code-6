"""
模块
"""
def prt(lst,is_tab=True,level=0):
        """代码"""
        for lst_tmp in lst:
                if isinstance(lst_tmp,list):
                        prt(lst_tmp,is_tab,level+1)                        
                else:
                        if is_tab:
                                for n in range(level):
                                        print('\t',end='')
                        print(lst_tmp)
