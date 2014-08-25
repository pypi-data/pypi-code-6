
    # <Music score creator. Generate a sheet music from an audio.>
    # Copyright (C) <2014>  <Jose Carlos Montanez Aragon>

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pyaudio
import wave
import time
import tempfile
from pylab import*
from scipy.io import wavfile
import numpy

class AudioData():
	def __init__(self):
		self.channels = 1
		self.format = pyaudio.paInt16
		self.rate = 8000
		self.frames = 0
		self.chunk = 2000
		self.record_seconds = 1
		self.sample_size = 0
		self.quarter_note_minute = 60 
		self.measure = '4/4'

# Range for each note
conversion = [(10000.0,1077.0,"r"),
			(1077.0,1017.1,"c''"),
			(1017.0,960.0,"b''"),	
			(960.0,906.2,"ais''"),
			(906.2,855.3,"a''"),
			(855.3,807.3,"gis''"),
			(807.3,762.0,"g''"),
			(762.0,719.2,"fis''"),
			(719.2,678.9,"f''"),
			(678.9,640.8,"e''"),
			(640.8,604.8,"dis''"),
			(604.8,570.8,"d''"),
			(570.8,538.8,"cis''"),
			(538.8,508.6,"c''"),
			(508.6,480.0,"b'"),
			(480.0,453.1,"ais'"),
			(453.1,427.7,"a'"),
			(427.7,403.6,"gis'"),
			(403.6,381.0,"g'"),
			(381.0,359.6,"fis'"),
			(359.6,339.4,"f'"),
			(339.4,320.4,"e'"),
			(320.4,302.4,"dis'"),
			(302.4,285.4,"d'"),
			(285.4,269.4,"cis'"),
			(269.4,254.3,"c'"),
			(254.3,240.0,"b"),
			(240.0,226.5,"ais"),
			(226.5,213.8,"a"),
			(213.8,201.8,"gis"),
			(201.8,190.5,"g"),
			(190.5,179.8,"fis"),
			(179.8,169.7,"f"),
			(169.7,160.2,"e"),
			(160.2,0.0,"r")]


def tempo(audioData):
	quarter_note = audioData.quarter_note_minute/60.0 
	semiquaver = 4*quarter_note

	# Determining the size of the chunk. 
	# That is, the number of semiquaver for second
	audioData.chunk = int(ceil(2530 - 200*semiquaver))

	return audioData



def record(audioData):
	global sounddirectory
	p = pyaudio.PyAudio()

	stream = p.open(format=audioData.format,
	                channels=audioData.channels,
	                rate=audioData.rate,
	                input=True,
	                frames_per_buffer=audioData.chunk) #buffer

	print("* recording")

	frames = []

	# Record the audio
	for i in range(0, int(audioData.rate / audioData.chunk * audioData.record_seconds)):
	    data = stream.read(audioData.chunk)
	    frames.append(data) # 2 bytes(16 bits) per channel

	print("* done recording")

	# Setup some data
	audioData.sample_size = p.get_sample_size(audioData.format)
	stream.stop_stream()

	# The audio is saved to work with it later
	# We save in temp directory
	sounddirectory = tempfile.gettempdir() + "/" +time.strftime("%H%M%S")+".wav"
	wf = wave.open(sounddirectory, 'wb')
	wf.setnchannels(audioData.channels)
	wf.setsampwidth(p.get_sample_size(audioData.format))
	audioData.sample_size = p.get_sample_size(audioData.format)
	wf.setframerate(audioData.rate)
	wf.writeframes(b''.join(frames))
	wf.close()

	stream.close()
	p.terminate()
	return (stream, frames, sounddirectory)

def save(dirname, filename, soundfile, audioData):
	wf = wave.open(dirname+"/"+filename+".wav", 'wb')
	wf.setnchannels(audioData.channels)
	wf.setsampwidth(audioData.sample_size)
	wf.setframerate(audioData.rate)
	wf.writeframes(b''.join(audioData.frames))
	wf.close()

def play(soundfile, aData, sounddirectory):

	f = wave.open(sounddirectory,"rb")  
	p = pyaudio.PyAudio()  

	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
	                channels = f.getnchannels(),  
	                rate = f.getframerate(),  
	                output = True)  
	data = f.readframes(aData.chunk)  

	while data != '':  
	    stream.write(data)  
	    data = f.readframes(aData.chunk)  
  
	stream.stop_stream()  
	stream.close()   
	p.terminate()  

def audioProcessing(filename, audioData):
	list_of_freq = getListofFreq(filename, audioData)
	list_pre = preprocessingFreqs(list_of_freq, audioData)
	final_list = getNotes(list_pre, audioData)
	writeFile(final_list, audioData)
	os.system("lilypond -s score.ly")


def getListofFreq(filename, audioData):
	wf = wave.open(filename, 'rb')
	swidth = wf.getsampwidth()
	RATE = wf.getframerate()
	audioData = tempo(audioData)

	# Use a Blackman window
	window = numpy.blackman(audioData.chunk)

	# Read some data
	data = wf.readframes(audioData.chunk)
	# Find the frequency of each chunk
	list_of_freq = []
	while len(data) == audioData.chunk*swidth:

	    # Unpack the data and times by the hamming window
	    indata = numpy.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
	                                         data))*window
	    # Take the fft and square each value
	    fftData=abs(numpy.fft.rfft(indata))**2
	    # Find the maximum
	    which = fftData[1:].argmax() + 1
	    # Use quadratic interpolation around the max
	    if which != len(fftData)-1:
	        y0,y1,y2 = numpy.log(fftData[which-1:which+2:])
	        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
	        # Find the frequency and output it
	        thefreq = (which+x1)*RATE/audioData.chunk
	        list_of_freq.append(thefreq)
	    else:
	        thefreq = which*RATE/audioData.chunk
	        list_of_freq.append(thefreq)
	    # Read some more data
	    data = wf.readframes(audioData.chunk)

	return list_of_freq

def preprocessingFreqs(list_of_freq, audioData):

	# Transform the original freq to the note
	list_ = []
	for i in list_of_freq:
		for j in conversion:
			if j[1] < i <= j[0]:
				list_.append(j[2])

	# Remove the silent notes at the begin of the audio
	while (len(list_) > 0) and (list_[0] == 'r'):
		list_.remove('r')

	return list_

def getNotes(list_, audioData):
	# Calculate the number of pieces of audio per measure
	n = 0
	if audioData.measure == '2/4':
		#n = 2*int(round(audioData.quarter_note_minute*0.0667))
		n = 8
	if audioData.measure == '3/4':
		#n = 3*int(round(audioData.quarter_note_minute*0.0667))
		n = 12
	if audioData.measure == '4/4':
		#n = 4*int(round(audioData.quarter_note_minute*0.0667))
		n = 16

	# Fill the list with silent notes ('r') to have complete measure
	number_fill = len(list_) % n

	for j in range(number_fill):
		list_.append('r')

	# From the before list, we obtain the number of repetitions of
	# a same note in every measure
	aux_list = []
	j = 0
	for m in range(len(list_)/n):
		note = list_[j] 
		cont = 1

		for i in range(1,n):
			if list_[j+i] == note:
				cont = cont + 1
			else:
				aux_list.append((note, cont))
				cont = 1
				note = list_[j+i]

		aux_list.append((note, cont))

		j = j + n

	# Once we have this list, we need to transform it to can get
	# the appropiate notes

	final_list = []
	for m in aux_list:
		if m[1] == 1:
			final_list.append(m[0] + '16')

		if m[1] == 2:
			final_list.append(m[0] + '8')

		if m[1] == 3:
			final_list.append(m[0] + '8.')

		if m[1] == 4:
			final_list.append(m[0] + '4')

		if m[1] == 5:
			final_list.append(m[0] + '4')
			final_list.append(m[0] + '16')

		if m[1] == 6:
			final_list.append(m[0] + '4.')

		if m[1] == 7:
			final_list.append(m[0] + '4..')

		if m[1] == 8:
			final_list.append(m[0] + '2')

		if m[1] == 9:
			final_list.append(m[0] + '2')
			final_list.append(m[0] + '16')

		if m[1] == 10:
			final_list.append(m[0] + '2')
			final_list.append(m[0] + '8')

		if m[1] == 11:
			final_list.append(m[0] + '2')
			final_list.append(m[0] + '8')
			final_list.append(m[0] + '16')

		if m[1] == 12:
			final_list.append(m[0] + '2.')
		if m[1] == 13:
			final_list.append(m[0] + '2..')
		if m[1] == 14:
			final_list.append(m[0] + '2...')
		if m[1] == 15:
			final_list.append(m[0] + '2....')
		if m[1] == 16:
			final_list.append(m[0] + '1')


	return final_list

def writeFile(final_list, audioData):
	f = open('score.ly', "w")

	f.write("\score {\n\t\\version \"2.16.2\"{\n\t\t\\time 4/4\n\t\t\key c \major\n\t\t\\tempo 4 = ")
	f.write(str(audioData.quarter_note_minute) + "\n\t\t")
	for i in (final_list):
		f.write(i)
		f.write(" ")
	f.write("\\bar \"|.\"\n\t}\n}\n")

	f.close()
