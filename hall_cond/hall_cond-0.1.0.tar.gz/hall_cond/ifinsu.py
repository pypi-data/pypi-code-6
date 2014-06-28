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
def initmm( ham ):
	
	eigenvalues, _ = np.linalg.eigh( ham )
	index = eigenvalues.argsort()
	eigenvalues = eigenvalues[ index ]
	size = eigenvalues.shape[0]
	mmband = np.array([[eigenvalues[i],eigenvalues[i]] for i in range(size)])

	return mmband

def updatemm( eigenvalues, mmband ):

	size = eigenvalues.shape[0]
	for i in range( size ):
		tmp = eigenvalues[i]

		# mininum
		if mmband[i][0] > tmp:
			mmband[i][0] = tmp
		# maximum
		if mmband[i][1] < tmp:
			mmband[i][1] = tmp

def ifin( mmband ):

	size = mmband.shape[0]
	insu = [0] * ( size - 1 )

	for i in range( size - 1 ):
		if mmband[i+1][0] - mmband[i][1] < 1.0/1000 :
			insu[i] = 1
		else:
			insu[i] = 0

	return np.array( insu )

def gap( mmband ):

	size = mmband.shape[0] - 1
	diff = np.zeros(size)

	for i in range( size ):
		diff[i] = mmband[i+1][0] - mmband[i][1]
	
	return diff

#def test():
#	mmband = np.array([[4.4,5.4],[5.5,5.6],[5.4,6.5]]) 
#	print( diffmm( mmband ))
#
#test()
