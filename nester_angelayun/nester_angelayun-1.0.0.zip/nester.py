# 2014/07/05 遞迴/function 實作
""" Learning python (深入淺出Python)
    Chapter 1-5 """

def deeperitem (inputlist):
	for eachitem in inputlist:
		if isinstance(eachitem, list):
			deeperitem(eachitem)
		else:
			print(eachitem)
