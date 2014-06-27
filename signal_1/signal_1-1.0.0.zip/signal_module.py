import numpy as np
def saw_tooth(n0,n1,n2):
        num=0
	if n0<n1 or n2<n1 or n2<n0:
		print 'Error'
	else:
		n=np.arange(n1,n2+1)
		x=np.zeros(len(n))
		no = np.arange(len(n))
		for a in no:
			if a < n0-n1:
				x[a]=0
			else:
				x[a]=num
				num+=1
	return n,x

def step_seq(n0,n1,n2):
	if (n0<n1) or (n2<n1) or (n2<n0):
		print 'Error'
	else:
		n=np.arange(n1,n2+1)
		x=(n>=n0)*1.
	return n,x

def imp_seq(n0,n1,n2):
	if (n0<n1) or (n2<n1) or (n2<n0):
		print 'Error'
	else:
		n=np.arange(n1,n2+1)
		x=(n==n0)*1.
	return n,x

n,x=imp_seq(-2,-3,5)

