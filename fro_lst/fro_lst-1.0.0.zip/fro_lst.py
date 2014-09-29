"""
模块
"""
def prt(lst):
        """代码"""
        for lst_tmp in lst:
                if isinstance(lst_tmp,list):
                        prt(lst_tmp)
                else:
                        print(lst_tmp)
