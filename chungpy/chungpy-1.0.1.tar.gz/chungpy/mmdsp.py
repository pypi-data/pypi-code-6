import numpy as np
import sys #for DEBUG only
import chungpy.mdsp

class mmdsp(chungpy.mdsp):
	"""Maximum and Minimum Density Segment Problem Instance

		Initiation of problem instance with concurrent solution of the corresponding Maximum AND Minimum Density Segment Problem

		Args:
			vals (list of numerical values): list of values
			widths (list of numerical values): list of width values
			min_width (numerical): minimum width of maximum density segments (default 1)
			max_width (numerical): maximum width of maximum density segments (default sum(widths))
			min_cont (int): minimum content, i.e. length, of maximum density segments (default 1)
			max_cont (int): maximum content, i.e. length, of maximum density segments (default len(vals))
		
		Attributes:
			vals (list of numerical values): list of values
			widths (list of numerical values): list of width values
			length (int): length of vals, i.e. length of widths
			min_width (numerical): minimum width of maximum density segments (default 1)
			max_width (numerical): maximum width of maximum density segments (default sum(widths))
			min_cont (int): minimum content, i.e. length, of maximum density segments (default 1)
			max_cont (int): maximum content, i.e. length, of maximum density segments (default len(vals))
			result_inds (dict of ints): mapping of stop indices to the corresponding start index of the corresponding maximum density segment
			max_dens (float): density of the overall maximum density segment
			max_inds (set): stop positions of all overall maximum density segments
			min_result_inds (dict of ints): mapping of stop indices to the corresponding start index of the corresponding minimum density segment
			min_dens (float): density of the overall minimum density segment
			min_inds (set): stop positions of all overall minimum density segments
	"""

	def __init__(self, vals, widths, min_width=None, max_width=None, min_cont = None, max_cont=None):
		
		self.length = len(vals)
		
		###CHECK INPUT PARAMETERS
		if len(widths)!=self.length: raise ValueError('ABORTING due to len(vals)={} & len(widths)={}'.format(len(vals), len(widths)))
		
		#check parameters (min_cont and max_cont)
		#TODO check type of min_cont, max_cont (Perhaps don't do the checks below, just output no results)
		if not min_cont:
			self.min_cont =1
		elif 0<min_cont<=self.length:
			self.min_cont = int(min_cont)
		else: raise ValueError('Illegal Minimum Content Parameter: {}'.format(min_cont))
		if not max_cont:
			self.max_cont = self.length
		elif self.min_cont<=max_cont<=self.length:
			self.max_cont = int(max_cont)
		else: raise ValueError('Illegal Maximum Content Parameter: {} (for Minimum Content {})'.format(max_cont, min_cont))

		#validity of min_width and max_width is checked during computation (otherwise all widths had o be summed up pevious to computations)
		if not min_width:
			self.min_width = 1
		elif (not max_width and 0<min_width) or 0<min_width<=max_width: self.min_width = min_width
		else: raise ValueError('Illegal Minimum Width Parameter: {}'.format(min_width))
		self.max_width = max_width
		if max_width and max_width < self.min_width:raise ValueError('Illegal Maximum Width Parameter: {}'.format(max_width))
		if not max_width: self.max_width = np.inf #TODO: check: this should be overall sum

		self.vals = np.array(vals, dtype=np.float)
		self.widths = np.array(widths, dtype=np.float)

		self.prefix_width_sum = np.zeros(self.length+1) #leading 0 due to width and density computation
		self.prefix_vals_sum = np.zeros(self.length+1)
		self.prefix_width_sum[1], self.prefix_vals_sum[1] = self.widths[0], self.vals[0]
		self.prefix_vals_sum[2:] = np.NAN
		self.prefix_vals_ind = 2 #from where to start prefix computation
		###MIN
		self.min_prefix_vals_sum = np.zeros(self.length+1)
		self.min_prefix_vals_sum[1] = -self.vals[0]
		self.min_prefix_vals_sum[2:] = np.NAN
		self.min_prefix_vals_ind = 2
		###
		self.prefix_width_ind = 2 #from where to start prefix computation
		

		# j0 Computation
		self.cutoff = 0
		self.j_0, tmp_cutoff = self.compute_j0(0)
		if tmp_cutoff:
			j_0 = self.j_0
			while tmp_cutoff and tmp_cutoff+self.cutoff<self.length and self.min_cont<=self.length-(tmp_cutoff+self.cutoff):
				self.cutoff += tmp_cutoff
				self.j_0=j_0
				j_0, tmp_cutoff = self.compute_j0(self.cutoff)
			else: self.j_0 = j_0

		#sys.stderr.write('j0={}, cutoff={}\n'.format(self.j_0,self.cutoff))

		#this is output for the user (or wrapper script)
		self.result_inds = dict()
		self.max_dens = -np.inf
		self.max_inds = set()
		###MIN
		self.min_result_inds = dict()
		self.min_dens = np.inf
		self.min_inds = set()
		#######

		if self.j_0:

			######## Algorithm GENERAL (linear-time)
			self.Phi = np.zeros(self.length+1,dtype=np.int) #one 1 added due to 1-based indexing and one due to UPADTE
			self.Psi = np.zeros(self.length+2,dtype=np.int) #one 1 added due to 1-based indexing and one due to UPADTE
			###MIN
			self.min_Phi = np.zeros(self.length+1,dtype=np.int)
			self.min_Psi = np.zeros(self.length+2,dtype=np.int) #one 1 added due to 1-based indexing and one due to UPADTE
			###
			
			self.p, self.q=1,1
			self.Phi[1] =1
			self.prev_rj =1 #TODO check if necessary
			self.lj=1
			i=1
			###MIN
			self.min_p, self.min_q=1,1
			self.min_Phi[1] =1
			min_i=1
			###

			#valid_ind_flag = False
			for j in range(self.j_0, self.length+1):
				

				#rj needed before UPDATE call
				#sys.stderr.write('max_width={}, max_cont={},l={}\n'.format(self.max_width, self.max_cont, self.length))
				if self.max_width==np.inf:
					if self.max_cont==self.length:
						lj=1
					else:
						lj = max(1,j-self.max_cont+1)
				else:
					lj = self.lj
					while ( self.width(lj,j) > self.max_width or j-lj+1 > self.max_cont) and lj<=j:
						lj+=1
						#no valid lj if lj>j
				if lj <=j and (self.width(lj,j)<self.min_width or j-lj+1<self.min_cont): lj=j+1
				#sys.stderr.write('lj: {}\n'.format(lj))
				if lj<=j:
					#valid lj found
					#new rj >= old rj
					if self.min_width==-np.inf:
						if self.min_cont==1:
							rj=j
						else:
							rj = max(lj,j-self.min_cont+1)
					else:
						rj = max(lj,self.prev_rj)
						#TODO
						while rj+1 <= j and self.width(rj+1,j)>= self.min_width and j-(rj+1)+1>= self.min_cont:
							rj+=1
							#maximum outcome rj=j
						if (self.width(rj,j)< self.min_width or j-rj+1<self.min_cont): rj+=1
					#sys.stderr.write('rj: {}\n'.format(rj))

				if lj <=j and rj <=j:

					self.lj=lj
					self.rj=rj
					
					self.minUPDATE(j)
					###
					while self.Phi[self.p] < self.lj:
						self.p+=1
					if i < self.Phi[self.p]:
						self.VARIANT(self.Phi[self.p],j)
					###MIN
					while self.min_Phi[self.min_p] < self.lj:
						self.min_p+=1
					if min_i < self.min_Phi[self.min_p]:
						self.minVARIANT(self.min_Phi[self.min_p],j)
					###
					
					i =self.LBEST(j)
					dj = self.dens(i,j)
					self.result_inds[j]=i
					if dj >= self.max_dens:
						if dj > self.max_dens:
							self.max_dens = dj
							self.max_inds=set([j])
						else:
							self.max_inds.add(j)
					###MIN
					min_i=self.minLBEST(j)
					#do not use mindens!!!!
					dj = self.dens(min_i,j)
					self.min_result_inds[j]=min_i
					if dj <= self.min_dens:
						if dj < self.min_dens:
							self.min_dens = dj
							self.min_inds=set([j])
						else:
							self.min_inds.add(j)
					###
					self.prev_rj = self.rj
					

	###HELPER FUNCS to GENERAL (linear-time)

	#MIN and MAX in one procedure
	def minUPDATE(self, j):
		for r in range(self.prev_rj+1, self.rj+1):
			while self.p < self.q and self.dens(self.Phi[self.q-1],self.Phi[self.q]-1) >= self.dens(self.Phi[self.q-1], r-1):
				self.q-=1
			self.q+=1
			self.Phi[self.q] =r
			#MIN
			while self.min_p < self.min_q and self.mindens(self.min_Phi[self.min_q-1],self.min_Phi[self.min_q]-1) >= self.mindens(self.min_Phi[self.min_q-1], r-1):
				self.min_q-=1
			self.min_q+=1
			self.min_Phi[self.min_q] =r


	def minVARIANT(self, r, y0):
		# l, y1 computation in O(r-l+y1-y0+1) 
		l = r
		while self.width(l-1,y0) <= self.max_width and l>1 and y0-l+2<=self.max_cont: l=l-1
		y1 = y0
		#take care of max_cont in y1 computation!!!
		#thresh for content constraints
		thresh=min(r+self.max_cont-1,self.length)
		while y1<thresh and self.width(r,y1+1)<=self.max_width: y1+=1
#		sys.stderr.write('y0=' + str(y0)+ ', y1=' + str(y1) + ', l=' + str(l)+'\n')
		self.minINIT(l,r-1)
		x = l
		ly=l
		for y in range(y0,y1+1):
			#TODO max computation
			while self.width(ly,y) > self.max_width: ly+=1
			x = self.minVBEST(max(max(x,ly),y-self.max_cont+1),r,y)
			#do not use mindens!!!!
			dj = self.dens(x,y)
			self.min_result_inds[y] = x
			if dj <= self.min_dens:
				if dj < self.min_dens:
					self.min_dens = dj
					self.min_inds=set([y])
				else:
					self.min_inds.add(y)


	def minINIT(self, l, r):
		self.min_Psi[r] =r
		for s in reversed(range(l,r)):
			t=s
			while t<r and self.mindens(s,t) >= self.mindens(s, self.min_Psi[t+1]):
				t = self.min_Psi[t+1]
			self.min_Psi[s] = t


	def minVBEST(self, l, r, y):
			x=l
			while x < r and self.mindens(x, self.min_Psi[x]) <= self.mindens(x,y):
				x = self.min_Psi[x]+1
			return x


	def minLBEST(self, j):
		while self.min_p<self.min_q and self.mindens(self.min_Phi[self.min_p], self.min_Phi[self.min_p+1]-1) <= self.mindens(self.min_Phi[self.min_p], j):
			self.min_p+=1
		return self.min_Phi[self.min_p]

	#########OTHER FUNCS####
	def __str__(self):
		out='# Overview\na = '
		if self.length>10:
			out+= '[' + ', '.join([str(self.vals[x]) for x in range(5)]) + ' ... ' + ', '.join([str(self.vals[x]) for x in range(self.length-5,self.length)]) + ']\n'
			out+= 'w = [' + ', '.join([str(self.widths[x]) for x in range(5)]) + ' ... ' + ', '.join([str(self.widths[x]) for x in range(self.length-5,self.length)]) + ']\n'
		else:
			out+='['+', '.join([str(x) for x in self.vals]) + ']\n'
			out+='w = ['+', '.join([str(x) for x in self.widths]) + ']\n'
		out+='length = ' +str(self.length) +'\n'
		out += 'min/max content = ' + str(self.min_cont) + ',' + str(self.max_cont) + '\n'
		out += 'min/max width = ' + str(self.min_width) + ',' + str(self.max_width) + '\n\n'
		
		if self.result_inds or self.min_result_inds:
			if self.result_inds:
				out+= '# Maximum Density Segment per Position\n'
				for stop in sorted(self.result_inds):
					out+= '{} -> {}, c={}, w={}, d={}\n'.format(self.result_inds[stop], stop, stop-self.result_inds[stop]+1,self.width(self.result_inds[stop],stop), self.dens(self.result_inds[stop],stop))
				out+='\n# Maximum Density Segment(s)\n'
				for stop in sorted(self.max_inds):
					out+= '{} -> {}, c={}, w={}, d={}\n'.format(self.result_inds[stop], stop, stop-self.result_inds[stop]+1,self.width(self.result_inds[stop],stop), self.dens(self.result_inds[stop],stop))
			if self.min_result_inds:
				out+= '\n# Minimum Density Segment per Position\n'
				for stop in sorted(self.min_result_inds):
					out+= '{} -> {}, c={}, w={}, d={}\n'.format(self.min_result_inds[stop], stop, stop-self.min_result_inds[stop]+1,self.width(self.min_result_inds[stop],stop), self.dens(self.min_result_inds[stop],stop))
				out+='\n# Minimum Density Segment(s)\n'
				for stop in sorted(self.min_inds):
					out+= '{} -> {}, c={}, w={}, d={}\n'.format(self.min_result_inds[stop], stop, stop-self.min_result_inds[stop]+1,self.width(self.min_result_inds[stop],stop), self.dens(self.min_result_inds[stop],stop))


		else:
			out+= 'NO FEASIBLE SEGMENTS\n'

		return out

	######## HELPER FUNCS ###############

	def mindens(self, start, stop):
		#TODO check indices
		if stop>self.min_prefix_vals_ind-1:
			for i in range(self.min_prefix_vals_ind,stop+1):
				self.min_prefix_vals_sum[i] = self.min_prefix_vals_sum[i-1]-self.vals[i-1] #CARE: self.widths is 0-based
			self.min_prefix_vals_ind=stop+1
		return (self.min_prefix_vals_sum[stop] - self.min_prefix_vals_sum[start-1])/self.width(start,stop)


if __name__ == "__main__":
	inst = mmdsp([72, -47, -9, -17, -88, 93, 74, 63, 87, -48 , -47, -9, -17, -88, 93, 74, 63, 87, -48],[86, 52, 56, 5, 40, 44, 50, 90, 28, 85, 52, 56, 5, 40, 44, 50, 90, 28, 85],max_cont=3, min_width=102, max_width=361)
	print(inst)

