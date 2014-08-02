"""
Classes for easy interpolation of trajectories and Curves.
Requires Scipy installed.
"""


class Interpolator:
	""" Poorman's linear interpolator, doesn't require Scipy. """

    def __init__(tt, ss, left=np.nan, right=np.nan):
    	self.tt = np.array(tt)
    	self.ss = np.array(ss)
    	self.left = left
    	self.right = right
    	self.tmin, self.tmax = min(tt), max(tt)

    def __call__(self, t):
    	if (t < self.tmin):
    		return self.left
    	if (t > self.tmax):
    		return self.right
    	ind = np.diff((self.ss >= t)).nonzero()[0]
        t1, t2 = self.tt[ind], self.tt[ind+1]
        s1, s2 = self.ss[ind], self.ss[ind+1]
    	return ((t-t1)*s2 + (t2-t)*s1)/(t2-t1)





class Trajectory:

	def __init__(self, tt, xx, yy):

		self.tt = tt
		self.xx = xx
		self.yy = yy
		self.udpate_interpolators()

    def __call__(self, t):
    	return (self.xi(t), self.yi(t))
    	
	def update_interpolators(self):
	    self.xi =  Interpolator(self.tt, self.xx)
	    self.yi =  Interpolator(self.tt, self.yy)
