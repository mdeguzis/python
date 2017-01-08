#!/usr/bin/python

# Demonstrates nested sequences
# start empty list
# written in python 2

# use this for ideal sorting of nested sequences
from operator import itemgetter

scores = []

choice = None

while choice != "0":

	print(
	"""
	High Scores

	0 - Exit
	1 - list scores
	2 - Add a score
	""")

	choice = raw_input("Choice: ")
	print ""

	# exit sequence
	if choice == "0":
		print "Good bye."

	elif choice == "1":
		print "High scores\n"
		print "Name\tSCORE"
		for entry in scores:
			score, name = entry
			print name, "\t", score

	elif choice == "2":
		name = raw_input("What was the players name?: ")
		score = int(raw_input("What score did the player get?: "))
		# here we want to use score first so we can sorth the list 
		# easily. You can use itemgetter library or a lamba to 
		# sort nested sequences as well.
		entry = (score,name)
		scores.append(entry)
		scores.sort(reverse=True)
		# This here keeps the high scores to a list of 5	
		scores = scores [0:5]
	else:
		print "Sorry that choice does not exist."


