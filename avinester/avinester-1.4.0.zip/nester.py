"""nester.py with tabCount"""
import sys
def print_item(the_list, indent=False, tabCount=0, fh=sys.stdout):
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_item(each_item, indent, tabCount+1,fh)
                else:
                        if indent:
                                for tab_stop in range(tabCount):
                                        print("\t",end='',file=fh)
                        print(each_item, file=fh)
