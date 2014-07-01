import os
import random
import sys
import itertools
import timeit
import datetime
import sfile
import stack
import errors

def prompt(write, tic=None):
	action = raw_input("> ")
	
	try:
		if action.lower() == 'q':
			
			if write:
				print '-' * 29 
				toc = timeit.default_timer()
				elapsed = toc - tic
				elapsed = int(elapsed)
				print "Elapsed time: %s h:mm:ss" % str(datetime.timedelta(seconds=elapsed)), '\n'

			exit(0)

	except ValueError:
		pass


def display(files, card_random, write, reverse, stack_random):


	stacks = sfile.read_stack_files(files)
	stacks.sort()

	cards = [a_stack[2] for a_stack in stacks] 

	for c in cards:
		if len(c) < 1:
			cards.remove(c)
	
	if len(cards) < 1:
		errors.id(7)

	print """
	Type 'Q' to stop anytime, RETURN to continue studying.
	"""
	print "Your arguments:"
	print "random cards: %s, random stacks: %s, reverse: %s, write: %s" % (card_random, stack_random, reverse, write)

	tic = timeit.default_timer()

	if card_random:
		for s in cards:
			random.shuffle(s)
	else:
		stacks.sort()
	
	setup = [iter(s) for s in cards]

	key = 0 

	prompt(write,tic)

	while True:
		
		rand_key = random.randrange(0, len(setup))
		rand_stack = setup[rand_key]

		try:
			if stack_random:
				a_card = next(rand_stack)

			else:
				try:
					a_card = next(setup[key])
				except IndexError:
					setup = [iter(s) for s in cards]
					key = 0
					continue

		except StopIteration:

			if card_random:
				for s in cards:
					random.shuffle(s)
				setup = [iter(s) for s in cards]
				key += 1
				continue


			elif not stack_random:
				key += 1
				continue

			else:
				setup = [iter(s) for s in cards]


		side1 = 1
		side2 = 2

		if reverse:
			side1 = 2
			side2 = 1

		for a_stack in stacks:

			try:
				if a_card in a_stack[2]:
					stack_name = a_stack[1] 
					stack_number = a_stack[0]
					stack_count = len(a_stack[2])
			except UnboundLocalError:
				errors.id(7)

		os.system('cls' if os.name == 'nt' else 'clear')

		print '-' * 40
		print "Stack #%d: %s   Card: %d/%d" % (stack_number, stack_name[:15], a_card[0], stack_count)
		print '-' * 40,'\n'

		print a_card[side1]
		prompt(write, tic)
		print a_card[side2]
		prompt(write, tic)
