#!/usr/bin/python

# Demonstratres programmer-created functions
# Written for python 2

# global constants
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9

def instructions():

	"""Display game instructions."""

	print \
	"""
	Welcome to the greatest intellectual challenge of all time: Tic-Tac-Toe.
	This will be a showdown between your human brain and my silicon processor.
	You will make your move known by entering a number, 0 - 8.
	The number
	will correspond to the board position as illustrated:
	0 | 1 | 2
	---------
	3 | 4 | 5
	---------
	6 | 7 | 8
	Prepare yourself, human.
	The ultimate battle is about to begin.
	"""

def ask_yes_no(question):
	"""Ask a yes or no question"""
	response = None
	while response not in ("y", "n")
		response = raw_input(question).lower()
	return response

def pieces():
		"""Determine if player or computer goes first."""
		go_first = ask_yes_no("Do you require the first move? (y/n): ")
		if go_first == "y":
				print "\nThen take the first move. You will need it."
				human = X
				computer = O
			else:
				print "\nYour bravery will be you undoing... I will go first."
				computer = X
				human = O
			return computer, human
def new_board():
	"""Create new game board."""
	board = []
	for square in range(NUM_SQUARES):
		board.append(EMPTY)
	return board

# main
print "Here are the instructions to the Tic-Tac-Toe game:"
instructions()

raw_input("\n\nPress the enter key to exit.")


			
