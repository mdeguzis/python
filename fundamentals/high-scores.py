#!/usr/bin/python

# Demonstrates list methods
# start empty list
# written in python 2

scores = []

choice = None

while choice != "0":

	print(
	"""
	High Scores

	0 - Exit
	1 - Show scores
	2 - Add a score
	3 - Delete a score
	4 - Sort scores
	""")

	choice = raw_input("Choice: ")
	print ""

	# exit sequence
	if choice == "0":
		print "Good bye."

	elif choice == "1":
		print "High scores"
		for score in scores:
			print score

	elif choice == "2":
		score = int(raw_input("What score did you get?: "))
		scores.append(score)

	elif choice == "3":
		score = int(raw_input("Remove which score?: "))
		if score in scores:
			scores.remove(score)
		else:
			print score, "isn't in the high scores list."

	elif choice == "4":
		# The default is Asc -> Desc, so reverse it.
		scores.sort(reverse=True)

	else: 
		print "Sorry that choice does not exist."


