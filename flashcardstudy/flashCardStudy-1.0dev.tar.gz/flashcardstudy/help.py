def gethelp():
	print """
	-h, --help: See this screen

	File-based arguments	
	--------------------

	-d, --display: Start session in with cards in order. 
	
	You always need to pass `-d` or `--display` and stack file(s) (*.stk) to
	start session, except `-a` (see below).

	Optional arguments:
	-r, --random: Will display cards in random order.
	-s, --stack: Jumps between stacks randomly. 
	-v, --reverse: Shows side two of card(s) first.
	-w, --write: Will display time log when the session is over. 

		Example: `python flashcard.py mystack.stk -d -r`

		This will launch flashcard with only one stack file
		named `mystack.stk' and it will display cards
		in random order. 
	
	-a, --all: Automatically passess all stack files in current dir. Use
		instead of `-d`. You can combine this with optional args.
	
		Example: `python flashcard.py -a -r -s`

		Will display all stacks in current dir in random order, stacks
		and cards are also shuffled.

	General arguments	
	-----------------
	You can't pass stack files when using these args:

	-n, --new: Create new stack (with cards).
	-l, --list: List stack(s) in current dir.
	-o, --order: Only for changing order of stacks in current dir.
	--author: Author info.

		Example: 'python flashcard.py -n`

		Launches flashCardStudy in a mode that allows you to create
		new stack and add cards into that stack.
	
	Edit argument
	-------------
	You can combine `-e` or `--edit` with only single stack file. It is
	used to edit given stack file.
"""

def author():
	print"""
	2014 comatory
	web: comatory.github.io
	twitter: @cmdspacenet

	Thanks to Luke Maurits for his module PrettyTable.

	"""
