#!/usr/bin/python

# Demonstratres programmer-created functions
# Written for python 2

# import 'print()' from future to make this work with python 2
from __future__ import print_function

# global constants
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9

def display_instruct():

	"""Display game instructions."""

	print(
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
	)

def ask_yes_no(question):
	"""Ask a yes or no question"""
	response = None
	while response not in ("y", "n"):
		response = raw_input(question).lower()
	return response

def ask_number(question, low, high):
	"""Ask for a number within a range."""

	response = None
	while response not in range(low, high):
		response = int(input(question))
	return response

def pieces():
		"""Determine if player or computer goes first."""
		go_first = ask_yes_no("Do you require the first move? (y/n): ")
		if go_first == "y":
			print("\nThen take the first move. You will need it.")
			human = X
			computer = O
		else:
			print("\nYour bravery will be you undoing... I will go first.")
			computer = X
			human = O
		return computer, human

def new_board():
	"""Create new game board."""

	# This function creates a new board (a list) with all nine elements 
	# set to EMPTY and returns it
	board = []
	for square in range(NUM_SQUARES):
		board.append(EMPTY)
	return board

def display_board(board):
	"""Display game board on screen."""

	# This function displays the board passed to it. Since each element in the 
	# board is either a space,the character "X" , or the character "O" , the 
	# function can print each one
	print("\n\t", board[0], "|", board[1], "|", board[2])
	print("\t", "---------")
	print("\t", board[3], "|", board[4], "|", board[5])
	print("\t", "---------")
	print("\t", board[6], "|", board[7], "|", board[8], "\n")

def legal_moves(board):
	"""Create list of legal moves."""

	# This function receives a board and returns a list of legal moves. This 
	# function is used by other functions.
	moves = []
	for square in range(NUM_SQUARES):
		if board[square] == EMPTY:
			moves.append(square)
	return moves

def winner(board):
	"""Determine the game winner."""
	
	# list possible conditions X or O can create tic-tac-toe
	WAYS_TO_WIN = ((0, 1, 2),
	(3, 4, 5),
	(6, 7, 8),
	(0, 3, 6),
	(1, 4, 7),
	(2, 5, 8),
	(0, 4, 8),
	(2, 4, 6))
	
	for row in WAYS_TO_WIN:
	# Check each element of the list for a winning combination
	# If there is a match (i.e. 3 x's or o's), indicate win
		if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY:
			winner = board[row[0]]
			return winner

	# Check for a tie
	if EMPTY not in board:
		return TIE

	# If there is no tie, and other conditions have not met, there is
	# no winner yet
	return None

def human_move(board, human):
	"""Get human move."""
	legal = legal_moves(board)
	move = None
	while move not in legal:
		move = ask_number("Where will you move? (0 - 8):", 0, NUM_SQUARES)
		if move not in legal:
			print("\nThat square is already occupied, foolish human. Choose another.\n")
	print("Fine...")
	return move

def computer_move(board, computer, human):
	"""Make computer move"""
	# == Basic AI ==
	# 1. If there's a move that allows the computer to win this turn, the computer
	#    should choose that move.
	# 2. If there's a move that allows the human to win next turn, the computer
	#    should choose that move.
	# 3. Otherwise, the computer should choose the best empty square as its move
	#    The best square is the center. The next best squares are the corners. 
	#    And the next best squares are the rest.

	# make a copy to work with since function will be changing list
	board = board[:]

	# the best positions to have, in order
	BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)

	print("I shall take square number", end= "")

	# create a list of legal moves
	# If the computer can win, then that's the move to make
	# If the computer makes a mistake, undo the move

	# if computer can win, take that move
	for move in legal_moves(board):
		board[move] = computer
		if winner(board) == computer:
			print(move)
			return move
		# done checking this move, undo it
		board[move] = EMPTY

	# At this point, it means the computer can't win on it's next move
	# Check if player can win on next move by looping through their moves left
	# If human can win, then that's the move to take for a block
	# Otherwise, undo the move and try the next legal move
	# if human can win, block that move
	for move in legal_moves(board):
		board[move] = human
		if winner(board) == human:
			print(move)
			return move
		# done checking this move, undo it
		board[move] = EMPTY

	# If we get this far, neither side can win on it's next move
	# Look in list of "best moves" and take the first legal one
	# since no one can win on next move, pick best open square
	for move in BEST_MOVES:
		if move in legal_moves(board):
			print(move)
			return move

def next_turn(turn):
	"""Switch turns."""
	if turn == X:
		return O
	else:
		return X

def congrat_winner(the_winner, computer, human):
	"""Congratulate the winner."""
	if the_winner != TIE:
		print(the_winner, "won!\n")
	else:
		print("It's a tie!\n")
	if the_winner == computer:
		print("As I predicted, human, I am triumphant once more.\n" \
			  "Proof that computers are superior to humans in all regards.")
	elif the_winner == human:
		print("No, no! It cannot be! Somehow you tricked me, human. \n" \
			  "But never again! I, the computer, so swear it!")
	elif the_winner == TIE:
		print("You were most lucky, human, and somehow managed to tie me. \n" \
			   "Celebrate today... for this is the best you will ever achieve.")
# main

def main():
	display_instruct()
	computer, human = pieces()
	turn = X
	board = new_board()
	display_board(board)

	while not winner(board):
		if turn == human:
			move = human_move(board, human)
			board[move] = human
		else:
			move = computer_move(board, computer, human)
			board[move] = computer
		display_board(board)
		turn = next_turn(turn)

	the_winner = winner(board)
	congrat_winner(the_winner, computer, human)
				

# start program
main()

raw_input("\n\nPress the enter key to quit.")

