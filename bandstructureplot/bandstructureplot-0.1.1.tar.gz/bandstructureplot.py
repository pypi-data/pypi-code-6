#
#   Copyright (C) 2014 Shudan Zhong
#
# This file is part of bandstructureplot.

# bandstructureplot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# bandstructureplot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with bandstructureplot.  If not, see <http://www.gnu.org/licenses/>.




# Plot the bandstructure for a specific hamiltonian along given lines
# 
#

import matplotlib.pyplot as plt
import numpy as np

VERSION = (0,1,1)
__version__ = ".".join(map(str, VERSION))


# plot the eigenvalues along the line connecting the two points
# 
# num_steps is the steps to take from the starting point to the end point
#
# eg. two_points_line_plot( numpy.array(([[0, 0, 0], [1, 0, 0]]), 20, ham, array )
#
def two_points_line_plot( points, num_steps, hamiltonian, argham ):

	eigenvalues_list = []
	#step = [ (points[1][i] - points[0][i]) / float(num_steps) for i in range( points.shape[1] ) ]

        step = ( points[1] - points[0] ) / num_steps

	# generate a set of points along the line and get their eigenvalues
	temp_point = copy.copy( points[0] )

	for i in range( num_steps ):

                arg = temp_point.tolist()
                arg.extend( argham )

		eigenvalues_list.append( np.sort( np.linalg.eigvalsh( hamiltonian( arg ) )))

		temp_point += step

	return eigenvalues_list

# plot the eigenvalues along lines connecting a list of points
#
def points_line_plot( points, num_steps, hamiltonian, argham ):

	# get the array of eigenvalues of each two points
	# append them together
	eigenvalues_list = []
	

	for i in range( points.shape[0] - 1 ): 

		eigenvalues_list.append( two_points_line_plot( np.array([points[i], points[i+1]]), num_steps, hamiltonian, argham ))

	# draw lines for each band

	eigenvalues_array = np.array( [segment for element in eigenvalues_list for segment in element] ) 

	# for test
#	plt.plot( eigenvalues_array.transpose() )
	# for test

	for i in range( eigenvalues_array.shape[1] ):

		plt.plot( eigenvalues_array.transpose()[i] )

	#plt.show()

