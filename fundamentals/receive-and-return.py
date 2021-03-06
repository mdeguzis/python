#!/usr/bin/python

# Demonstrates various combinations of receiving and returning values

def display(message):
	print(message)

def give_me_five():
	five = 5
	return five

def ask_yes_no(question):
		"""Ask a yes or no question."""
		response = None
		while response not in ("y", "n"):
				response = raw_input(question).lower()
				return response

# main
display("Heres a message for you.\n")

number = give_me_five()
print "Here's what I got from give_me_five(): ", number

answer = ask_yes_no("\nPlease enter 'y' or 'n': ")
print "Thanks for entering: ", answer

raw_input("\n\nPress ENTER to exit")
