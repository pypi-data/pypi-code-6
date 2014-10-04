import time
import sys


def visibleclock(n):
	for remaining in range(n, 0, -1):
		sys.stdout.write("\r")
		sys.stdout.write("{:2d} seconds remaining...".format(remaining))
		sys.stdout.flush()
		time.sleep(1)

	#because the line isn't being cleared, we need to ensure that that each new line of output is long enough to cover up the existing lines
	sys.stdout.write("\rComplete!                            \n")

if __name__ == "__main__":
	print "dog"
	visibleclock(10)