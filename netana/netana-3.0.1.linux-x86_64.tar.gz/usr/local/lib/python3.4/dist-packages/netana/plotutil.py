#!/usr/bin/env python3
# Python Module to plot the DC/AC Network Response

import os,sys,time
# the following lines where commented out as of
# netana version 1.0.1 dated 05 May 2014

# Next two lines are very Important in order to keep the plot window
# from freezing!!!
#from matplotlib import use
#if sys.platform[:5] == 'linux' :
	#use('GTKAgg')  # setup plotting backend for linux os
#else:
	#use('WXAgg')  # setup plotting backend for win32 os

from matplotlib import pyplot as plt

def matplot(fn='',units='Hz',ylab='None'):

	if units != '':
		matplotac(fn,units)
	else:
		matplotdc(fn,ylab)


def matplotdc(fn='', ylab='None'):
	""" This module formats the commands Matplotlib
	to plot the DC network valuse of a circuit. The only
	parameters required are the filename and the Y axis label.
	"""
	if ylab == 'Volts':
		xlab = 'Node Number'
	else:
		xlab = 'Mash Number'

	# Get data from the report data file.
	mag = []
	with open(fn, 'r') as datafile:
		for line in datafile:
			if line[0] in ['#','G'] or len(line) < 5 :
				continue
			else:
				sl = line.split()
				mag.append(sl[2])


	# Get basename of report file
	bfn = os.path.basename(fn)
	name = bfn[:bfn.find('.')] + '\n'
	plt.title(name)
	plt.ylabel(ylab)
	plt.xlabel(xlab)
	plt.grid(True)
	labs = range(1,len(mag)+1)
	plt.plot(labs, mag, 'r-o')

	# Add timestamp to plot
	ts = time.ctime()
	plt.figtext(0.02,0.015,ts,fontsize=7, ha='left')
	plt.show()


def matplotac(fn="",units='Hz'):
	"""
	This module formats the commands required by Matplotlib
	to plot the network analysis response/tansfer fuction
	of an AC network where the output report contains three cols of
	data in the following order: frequency, magnitude (dB),
	and phase angle (degrees).

	This function "matplotac" is called with file name of the data file
	to be plotted and the frequency units string such as Hz, Kz, Mz).
	The units argument defaults to 'Hz'.

	call as follows:  plotutil.matplotac(fn, units='Hz')
	"""



	# Get data from the report data file.
	freq = []
	mag = []
	pa = []
	with open( fn, 'r') as datafile:
		for line in datafile:
			if line[0] in [ '#','G' ] or len(line) < 5 :
				continue
			else:
				sl = line.split()
				freq.append(sl[0])
				mag.append(sl[1])
				pa.append(sl[2])

	plt.figure(1)
	plt.subplot(211)
	# Get basename of report file
	bfn = os.path.basename(fn)
	name = bfn[:bfn.find('.')] + '\n'
	plt.title(name)
	plt.ylabel('Gain (db)')
	plt.grid(True)
	plt.plot(freq, mag)

	plt.subplot(212)
	plt.ylabel('Phase Angle (Deg.)')
	plt.xlabel('Frequency (' + units[0] + units[1].lower() + ')')
	plt.grid(True)
	plt.plot(freq, pa)
	# Add timestamp to plot
	ts = time.ctime()
	plt.figtext(0.02,0.015,ts,fontsize=7, ha='left')
	plt.show()


if __name__ == "__main__":

	os.chdir('/home/jim/test')

	matplot("Wein_Bridge.report", "Hz")
##	matplot("BalencedTeeNetwork.report", "Hz")
##	matplot(fn="Bal_RC_Bridge.report", units="Hz")
##	matplot(fn="BainterFilter.report", units="Hz")
##	matplot(fn="LadderNode10.report", ylab="Volts")
##	matplot(fn="LadderMash9.report", ylab="Amps")
