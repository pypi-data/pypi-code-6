import random
import sys
from chungpy.mdsp import *
from chungpy.mmdsp import *

#def test_width():
#	for it in range(100):
#		l = random.randint(1, 100)
#		widths = random.sample(range(1,int(1e2)+1), l)
#		vals = random.sample(range(-int(1e2),int(1e2)), l)
#		#initialization
#		inst = mdsp(vals,widths)
#		if inst.j_0:
#			for i in range(inst.cutoff,l):
#				for j in range(i,l):
#					w = sum(widths[i:j+1])
#					assert inst.width(i+1,j+1)==w, '({},{}), inst.width(i,j)={}, width={}\n'.format(i,j,inst.width(i+1,j+1),w)

#def test_density():
#	for it in range(100):
#		l = random.randint(1, 100)
#		widths = random.sample(range(1,int(1e2)+1), l)
#		vals = random.sample(range(-int(1e2),int(1e2)), l)
#		#initialization
#		inst = mdsp(vals,widths)
#		if inst.j_0:
#			for i in range(inst.cutoff,l):
#				for j in range(i,l):
#					#sys.stderr.write('{}->{}\n'.format(i,j))
#					dens = sum(vals[i:j+1])/sum(widths[i:j+1])
#					#assert inst.dens(i-inst.cutoff+1,j-inst.cutoff+1)==dens, '({},{}), inst.dens(i,j)={}, dens={}\n'.format(i,j,inst.dens(i-inst.cutoff+1,j-inst.cutoff+1),dens)
#					assert inst.dens(i+1,j+1)==dens, '({},{}), inst.dens(i,j)={}, dens={}\n'.format(i,j,inst.dens(i+1,j+1),dens)

#def test_j0_computation():
#	for it in range(100):
#		l = random.randint(1, 100)
#		sys.stderr.write('#\nl={}\n'.format(l))
#		widths = random.sample(range(1,int(1e2)+1), l)
#		vals = random.sample(range(-int(1e2),int(1e2)), l)
#		sys.stderr.write('{}\n{}\n'.format(vals,widths))
#		max_cont = random.randint(1, l)
#		min_cont = random.randint(1,max_cont)
#		sys.stderr.write('min_/max_cont {}, {}\n'.format(min_cont, max_cont))
#		max_width = random.randint(1, sum(widths))
#		min_width = random.randint(1,max_width)
#		sys.stderr.write('min_/max_width {}, {}\n'.format(min_width, max_width))

#		#initialization
#		inst = mdsp(vals,widths,min_width=min_width, max_width=max_width,min_cont=min_cont, max_cont=max_cont)
#		inst2 = mdsp(vals,widths) #TEST instance
#		sys.stderr.write('j0={}\ncutoff={}\n'.format(inst.j_0,inst.cutoff))

#		if not inst.j_0:
#			#check every segment
#			#stop position
#			for j in range(min_cont, inst2.length+1):
#				#stop position
#				for i in range(max(1,j-max_cont+1), max(j-min_cont+1,1)+1):
#					assert not min_width<=inst2.width(i,j)<=max_width, 'None, None : ({}, {}), width={}\n'.format(i,j,inst.width(i,j))

#		elif inst.j_0 and not inst.cutoff:
#			loop_j=0
#			for i in range(1,inst.length-min_cont+2):
#				for j in range(i+min_cont-1, i+max_cont):
#					w=inst.width(i,j)
#					if inst.max_width and inst.min_width <= w <= inst.max_width:
#						assert j==inst.j_0, 'Found larger or smaller j ({}) than j_0!'.format(j)
#						break
#					elif inst.min_width <= w:
#						assert j==inst.j_0, 'Found larger or smaller j ({}) than j_0!'.format(j)
#						break
#				if inst.min_width <= w <= inst.max_width:
#					loop_j=j
#					break
#			assert loop_j==inst.j_0, 'Found larger j ({}) than j_0!'.format(loop_j)

#		else:
#			#inst.j_0 and cutoff
#			loop_i,loop_j = 0,0
#			for i in range(1,inst2.length-min_cont+2):
#				for j in range(i+min_cont-1, min(inst2.length,i+max_cont-1)+1):
#					w = inst2.width(i,j)
#					if min_width <= w <= max_width:
#						loop_j = j
#						loop_i = i
#						break
#				if min_width <= w <= max_width: break
#				#in case turn inst.j_0 to int for addition:
#				if not inst.j_0: inst.j_0 = 0
#			
#			#assert loop_i-1 == inst.cutoff and loop_j == inst.cutoff+inst.j_0, '{}\nloop_i={},loop_j={}\ninst: cutoff={},j0={}'.format(inst.widths, loop_i,loop_j, inst.cutoff, inst.j_0)
#			assert loop_i-1 == inst.cutoff and loop_j ==inst.j_0, '{}\nloop_i={},loop_j={}\ninst: cutoff={},j0={}'.format(inst.widths, loop_i,loop_j, inst.cutoff, inst.j_0)
			
def test_GENERAL():
	for it in range(1000):
		dim = int(1e2)
		l = random.randint(1, dim)
		sys.stderr.write('#\nl={}\n'.format(l))
		border = 10*dim
		widths = random.sample(range(1,border+1), l)
		vals = random.sample(range(-border,border), l)
		sys.stderr.write('{}\n{}\n'.format(vals,widths))
		max_cont = random.randint(1, l)
		min_cont = random.randint(1,max_cont)
		sys.stderr.write('min_/max_cont {}, {}\n'.format(min_cont, max_cont))
		max_width = random.randint(1, sum(widths))
		min_width = random.randint(1,max_width)
		sys.stderr.write('min_/max_width {}, {}\n'.format(min_width, max_width))

		#initialization
		inst = mdsp(vals,widths,min_width=min_width, max_width=max_width,min_cont=min_cont, max_cont=max_cont)
		inst2 = mdsp(vals,widths) #TEST instance
		result_inds = dict()
		max_dens = -float('Inf')
		inds = None
		for j in range(min_cont,inst2.length+1):
			for i in range(max(1,j-max_cont+1), max(1,j-min_cont+1)+1):
				if min_width <= inst2.width(i,j) <= max_width:
					d = inst2.dens(i,j)
					if d>max_dens:
						max_dens=d
						inds = (i,j)
		sys.stderr.write('max_dens='+str(max_dens)+', '+str(inds)+'\n')
		assert max_dens==inst.max_dens, 'max_dens={} AND inst.max_dens={}\n{}\n{}\n'.format(max_dens, inst.max_dens, inst.result_inds,inst.max_inds)


#def test_mmdsp():
#	for it in range(1000):
#		dim = int(1e2)
#		l = random.randint(1, dim)
#		sys.stderr.write('#\nl={}\n'.format(l))
#		border = 10*dim
#		widths = random.sample(range(1,border+1), l)
#		vals = random.sample(range(-border,border), l)
#		sys.stderr.write('{}\n{}\n'.format(vals,widths))
#		max_cont = random.randint(1, l)
#		min_cont = random.randint(1,max_cont)
#		sys.stderr.write('min_/max_cont {}, {}\n'.format(min_cont, max_cont))
#		max_width = random.randint(1, sum(widths))
#		min_width = random.randint(1,max_width)
#		sys.stderr.write('min_/max_width {}, {}\n'.format(min_width, max_width))

#		#initialization
#		inst = mmdsp(vals,widths,min_width=min_width, max_width=max_width,min_cont=min_cont, max_cont=max_cont)
#		sys.stderr.write('inst done\n')
#		inst2 = mmdsp(vals,widths) #TEST instance
#		result_inds = dict()
#		max_dens = -float('Inf')
#		min_dens = float('Inf')
#		inds = None
#		min_inds=None
#		for j in range(min_cont,inst2.length+1):
#			for i in range(max(1,j-max_cont+1), max(1,j-min_cont+1)+1):
#				if min_width <= inst2.width(i,j) <= max_width:
#					d = inst2.dens(i,j)
#					if d>max_dens:
#						max_dens=d
#						inds = (i,j)
#					if d < min_dens:
#						min_dens = d
#						min_inds = (i,j)
#		sys.stderr.write('max_dens='+str(max_dens)+', '+str(inds)+'\n')
#		sys.stderr.write('min_dens='+str(min_dens)+', '+str(min_inds)+'\n')
#		assert max_dens==inst.max_dens, 'max_dens={} AND inst.max_dens={}\n{}\n{}\n'.format(max_dens, inst.max_dens, inst.result_inds,inst.max_inds)
#		assert min_dens==inst.min_dens, 'min_dens={} AND inst.min_dens={}\n{}\n{}\n'.format(min_dens, inst.min_dens, inst.min_result_inds,inst.min_inds)




