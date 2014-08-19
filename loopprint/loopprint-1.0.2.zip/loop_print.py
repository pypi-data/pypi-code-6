"""This is sample test"""
stu=["David", 30, "Andy", 20, ["B1", "B2", ["C1", "C2"]]]
def list_check(arg11, intend = False, level=0):
	for check in arg11:
		if isinstance(check, list):
			list_check(check, intend, level+1)			
		else:
                        if intend:
                                for tab_stop in range(level):
                                        print("\t", end='')
                        print(check)
list_check(stu, False, 0)

		
