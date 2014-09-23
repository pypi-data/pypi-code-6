def showEachItem(alist, level=0, isShowTab = False):
	for eachItem in alist:
		if isinstanceof(eachItem, list):
			showEachItem(eachItem, level + 1, isShowTab)
		else:
			if isShowTab:
				print("\t" * level, end="")

