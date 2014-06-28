#
#   Copyright (C) 2014 Shudan Zhong
#
# This file is part of hall_cond.

# hall_cond is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# hall_cond is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with hall_cond.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import ifinsu

# calculate P = |u_nk><u_nk|
def proj_eigenvectors( bn, eigenvalues, eigenvectors ):

	# sort eigenvalues and eigenvectors from lowest to highest
	index = eigenvalues.argsort()
	eigenvalues = eigenvalues[ index ]
	eigenvectors = eigenvectors.transpose()[ index ]

	eigenvectors = eigenvectors[0:bn]
	proj = np.dot ( eigenvectors.transpose(), np.conj( eigenvectors ) )

	return np.array( proj )

def diff_proj( vec, direc, bn, hamiltonian, argham ):  
	"""
	calculate dP/dk 
	"""

	num  = 1000
	diff = 1.0/num 

	proj_plus  = proj_eigenvectors( bn, *np.linalg.eigh( hamiltonian(vec + diff*direc, argham )))
	proj_minus = proj_eigenvectors( bn, *np.linalg.eigh( hamiltonian(vec - diff*direc, argham )))

	diff_P = ( proj_plus - proj_minus ) / ( 2 * diff )

	return diff_P

def diff_vec( size, direc ):
	"""
	get the direction for differential 
	"""
	# identity matrix
	e_k = np.identity( size )

	# diff in selected directions
	if   direc == 'x':
		
		dvec = np.array([ e_k[i] for i in [1, 2] ])

	elif direc == 'y':

		dvec = np.array([ e_k[i] for i in [2, 0] ])

	elif direc == 'z':

		dvec = np.array([ e_k[i] for i in [0, 1] ])

	else:
		return None
	
	return dvec

# electron density 1
# hall conductivity 10
# insulator search for all bands 100
# total energy 1<<3
# density of states 1 << 4
def hall_cond_band( choice, reciprocal_vec, steps, fermi_energy, direc, hamiltonian, argham ):
	
	
	size       =  reciprocal_vec.shape[0]
	start_vec  =  np.zeros( size ) 
	step_k     =  np.array( [ reciprocal_vec[i] / float(steps[i]) for i in range(size) ] )
	dvec       =  diff_vec( size, direc ) 

	# energy break
	epsilon    =  1e-4
	

	conductivity = np.complex(0.0, 0.0)
	electrons	 = 0.0
	total_energy = 0.0
	result		 = []

	if choice & (1<<2) != 0:
		mmband = ifinsu.initmm( hamiltonian( np.zeros(3), argham ))
	
	if choice & (1<<4) != 0:

		num        =  10
		interval   =  np.copy( epsilon )
		upbound    =  fermi_energy + interval * num
		lowbound   =  fermi_energy - interval * num
		ds         =  [0.0] * 2 * num
	
	if choice & ( (1<<0) + (1<<3) + (1<<4) ) != 0:

		totalsteps = 1.0
		for i in range( steps.shape[0]):
			totalsteps *= steps[i]

	vec_list = [[ np.copy( start_vec ), 0 ] for i in range( step_k.shape[0] - 1 )]

	while vec_list[0][1] < steps[0]:

		vec = np.copy( vec_list[step_k.shape[0] - 2][0] )

		for i in range( steps[step_k.shape[0] - 1] ):

			ham_matrix  = hamiltonian( vec, argham )
			eigenvalues, eigenvectors = np.linalg.eigh( ham_matrix )
			# sort eigenvalues and eigenvectors from lowest to highest
			index       = eigenvalues.argsort()
			eigenvalues = eigenvalues[ index ]

			for m in range ( eigenvalues.shape[0] + 1 ):

				if m == eigenvalues.shape[0]:
					break

				if eigenvalues[m] - fermi_energy > epsilon: 
					break

			# electron density
			if choice & (1 << 0) != 0:

				electrons += m
			
			# hall conductivity
			if choice & (1 << 1) != 0:

				if m != 0:
					
					eigenvectors = eigenvectors.transpose()[ index ]

					eigenvectors = eigenvectors[0:m]
					proj = np.dot ( eigenvectors.transpose(), np.conj( eigenvectors ) )
					#proj = proj_eigenvectors( m, eigenvalues, eigenvectors )
					diff = [diff_proj( vec, dvec[q], m, hamiltonian, argham ) for q in range(2)]
					temp = np.trace(reduce( np.dot, [diff[0], proj, diff[1]] )) 
					conductivity += temp - np.conj( temp ) 
			
			# insulator search
			if choice & (1 << 2) != 0:
					
				ifinsu.updatemm( eigenvalues, mmband )

			# total energy
			if choice & (1 << 3) != 0:
				
				for i in range(m):

					total_energy += eigenvalues[i]

			# density of states near fermi energy
			if choice & (1<<4) != 0:

				p = np.copy(m)

				while p < eigenvalues.shape[0] and eigenvalues[p] < upbound :

					tmp      =  int( ( eigenvalues[p] - lowbound ) / interval )
					ds[tmp] +=  1
					p 		+=  1


				p = m - 1
				while p >= 0 and eigenvalues[p] > lowbound:

					tmp      =  int( ( eigenvalues[p] - lowbound ) / interval )
					ds[tmp] +=  1
					p 		-=  1


			vec +=  step_k[step_k.shape[0]-1]


		for i in reversed( range( step_k.shape[0] - 1 ) ):

			vec_list[i][1] += 1
			vec_list[i][0] += step_k[i]

			if vec_list[i][1] < steps[i] or i == 0:
				break

			vec_list[i][1] = 0
			vec_list[i][0] = step_k[i - 1] + vec_list[i - 1][0]
		
	if choice & (1<<0) != 0:

		result.append( electrons/float(eigenvalues.shape[0])/totalsteps )

	if choice & (1<<1) != 0:
		result.append( (-1j * conductivity / np.power( (2 * np.pi), size - 1 ) * np.linalg.det(step_k)).real )

	if choice & (1<<2) != 0:
		result.append( ifinsu.gap( mmband ) )
	
	if choice & (1<<3) != 0:

		result.append( total_energy / totalsteps / eigenvalues.shape[0]  )

	if choice & (1<<4) != 0:

		result.append( (np.array(ds) / totalsteps / eigenvalues.shape[0]).tolist() )

	return result 

#def part_conductivity_band( start_vec, steps, step_k, fermi_energy, direc, hamiltonian, argham ):
#	
#	conductivity = np.complex(0.0, 0.0)
#	electrons = 0.0
#
#	vec_list = [[ np.copy( start_vec ), 0 ] for i in range( step_k.shape[0] - 1 )]
#
#	while vec_list[0][1] < steps[0]:
#
#		vec = np.copy( vec_list[step_k.shape[0] - 2][0] )
#
#		for i in range( steps[step_k.shape[0] - 1] ):
#
#
#			eigenvalues, _ = np.linalg.eigh( hamiltonian( vec, *argham ) )
#
#			# sort eigenvalues and eigenvectors from lowest to highest
#			index = eigenvalues.argsort()
#			eigenvalues = eigenvalues[ index ]
#		
#			for m in range ( eigenvalues.shape[0] + 1 ):
#
#				if m == eigenvalues.shape[0]:
#					break
#
#				if eigenvalues[m] - fermi_energy > 1.0/1000:
#					break
#
#			electrons += m
#
#			#if m != 0:
#				#conductivity +=  diff_proj_diff( vec, direc, m, hamiltonian, argham )
#
#			vec +=  step_k[step_k.shape[0]-1]
#
#		for i in reversed( range( step_k.shape[0] - 1 ) ):
#
#			vec_list[i][1] += 1
#			vec_list[i][0] += step_k[i]
#
#			if vec_list[i][1] < steps[i] or i == 0:
#				break
#
#			vec_list[i][1] = 0
#			vec_list[i][0] = step_k[i - 1] + vec_list[i - 1][0]
#
#	#return conductivity, electrons/float(eigenvalues.shape[0])
#	#return conductivity
#	return electrons/float(eigenvalues.shape[0])
#
#def hall_cond_band( reciprocal_vec, steps, fermi_energy, direc, hamiltonian, argham ):
#
#	k       =  np.copy( reciprocal_vec )
#	starter =  np.zeros( k.shape[0] ) 
#
#
#	step_k = np.array( [ k[i] / float(steps[i]) for i in range(k.shape[0]) ] )
#	
#	# MPI
#	root_process = 0
#
#	from mpi4py import MPI
#	from mpi4py.MPI import ANY_SOURCE
#
#	comm = MPI.COMM_WORLD
#	size = comm.Get_size()
#	rank = comm.Get_rank()
#
#	if rank == root_process:
#
#		# calculate the conductivity in the segment assigned to root process
#		start_vec = starter + (size-1) * int(steps[0]/size) * step_k[0] 
#		steps[0]  = steps[0] - (size-1) * int(steps[0]/size) 
#
#		#conductivity, electrons = part_conductivity_band( start_vec, steps, step_k, fermi_energy, direc, hamiltonian, argham )
#		#conductivity = part_conductivity_band( start_vec, steps, step_k, fermi_energy, direc )
#		electrons = part_conductivity_band( start_vec, steps, step_k, fermi_energy, direc, hamiltonian, argham )
#
#		# collect the partial conductivity from slave processes
#		for i in range( 1, size ):
#
#			#partial_conductivity = comm.recv( source=MPI.ANY_SOURCE, tag=11 )
#			partial_electrons = comm.recv( source=MPI.ANY_SOURCE, tag=22 )
#			#conductivity += partial_conductivity
#			electrons += partial_electrons
#
#		total_electrons = 1.0
#		for i in range( steps.shape[0]):
#			total_electrons = total_electrons * steps[i]
#
#		#return [-1j * conductivity / (2 * np.pi) * np.linalg.det(step_k), electrons/total_electrons]
#		#return -1j * conductivity / np.power( (2 * np.pi), k.shape[0] - 1 ) * np.linalg.det(step_k), electrons/total_electrons
#		return electrons/total_electrons
#
#	else:
#		# slave process
#
#		steps[0]  = int( steps[0] / size )
#		start_vec = starter + (rank-1)*steps[0]*step_k[0]
#
#		#conductivity, electrons = part_conductivity_band( start_vec, steps, step_k, fermi_energy, direc, hamiltonian, argham )
#		#conductivity = part_conductivity_band( start_vec, steps, step_k, fermi_energy, direc )
#		electrons = part_conductivity_band( start_vec, steps, step_k, fermi_energy, direc, hamiltonian, argham )
#
#		#comm.send( conductivity, dest=root_process, tag=11 )
#		comm.send( electrons, dest=root_process, tag=22 )
#
#		sys.exit(0)
#
