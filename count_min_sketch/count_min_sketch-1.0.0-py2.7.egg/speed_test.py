import countminsketch
import count_min_sketch
from time import time
from random import randint
mytime = 0
theirtime = 0

mine = count_min_sketch.CountMinSketch(1000, 5000)
theirs = countminsketch.CountMinSketch(1000, 5000)

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