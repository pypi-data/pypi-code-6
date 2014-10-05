import countminsketch
import count_min_sketch
from time import time
from random import randint
mytime = 0
theirtime = 0

mine = count_min_sketch.CountMinSketch(1000, 5000, bits=1024)
theirs = countminsketch.CountMinSketch(1000, 5000)

def artificial_test():
	from string import letters
	letters = letters[:26]
	to_inc = [randint(5, 100) for letter in letters]

	for letter, incto in zip(letters, to_inc):

		for i in xrange(incto):
			t = time()
			mine.update(letter)
			mytime += time() - t
	
			t = time()
			theirs.add(letter)
			theirtime += time() - t

	for letter, should_be in zip(letters, to_inc):
		t = time()
		a = mine[letter]
		mytime += time() - t
	
		t = time()
		b = theirs[letter]
		theirtime += time() - t
	
		print a, b, a == b, a == should_be

	print mytime, theirtime
	print theirtime / mytime

def natural_test():
	from re import findall
	from collections import defaultdict
	from urllib2 import urlopen
	
	#Adventures of Sherlock Holmes
	story = urlopen('http://www.gutenberg.org/cache/epub/1661/pg1661.txt').read()
	tokens = findall('[a-z]{3,}', story)
	f = defaultdict(lambda: 0)
	mytime, theirtime = 0, 0
	for token in tokens:
		f[token] += 1
	for i, (token, freq) in enumerate(f.iteritems()):
		if (i+1)%500 == 0:
			print 100.*(i+1) / len(f)
		t = time()
		mine.update(token, freq)
		mytime += time() - t
		
		t = time()
		theirs.add(token, freq)
		theirtime += time() - t
	
	right= 0
	theirright = 0
	for token, freq in f.iteritems():
		theirright += theirs.query(token) == freq
		right += mine.query(token) == freq
	
	print 'my % correct:', 1.*right / len(f)
	print 'their % correct:', 1.*theirright / len(f)
	print mytime, theirtime, theirtime  / mytime

if __name__ == '__main__':
	natural_test()