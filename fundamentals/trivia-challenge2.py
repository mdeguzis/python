#!/usr/bin/python

# Trivia Challenge
# Trivia game that reads a plain text file

import sys
import pickle

def open_file(file_name, mode):
    """Open a file."""
    try:
        the_file = open(file_name, mode)
		
    except(IOError), e:
        print "Unable to open the file", file_name, "Ending program.\n", e
        raw_input("\n\nPress enter to exit..")
        sys.exit()
    else:
        return the_file

def next_line(the_file):
    """Return the next line from the trivia file, formatted."""
    line = the_file.readline()
    line = line.replace("/", "\n")
    return line

def next_block(the_file):
	"""Return the next block of data from the trivia file."""
	category = next_line(the_file)

	question = next_line(the_file)

	answers = []
	for j in range(4):
		answers.append(next_line(the_file))

	correct = next_line(the_file)

	# Need to index 'correct' here since 'correct' is a string with a newline
	# Correct[0] gets you the right string, the number, instead of '1\n'
	# Alternatively, just strip the newline with '.strip()' or '.rstrip('\n')'
	# strip() would allow answers that are not a single char

	if correct:
		#correct = correct[0]
		#correct = correct.strip()
		#correct = correct.strip('\n')
		correct = correct.rstrip('\n')

	points = next_line(the_file)
	if points:
		points = points.strip()

	explanation = next_line(the_file)
	return category, question, answers, correct, points, explanation

def welcome(title):
    """Welcome the player and get his/her name."""
    print "Welcome to Trivia Challenge!\n"
    print title

def print_high_scores(storage_type):
	"""loads a high scores file (if exists)"""

	# Try to laod the file, do nothing if it isn't there
	try:
		if storage_type is "pickle":
			with open("high-scores.dat", "rb") as scores:
				high_scores = pickle.load(scores)
				print "\nHigh Scores\n==============="
				for item in high_scores:
					print item
		elif storage_type is "plain_txt":
			with open('high-scores.txt', 'r') as scores:
				high_scores = scores.read().splitlines()
				print "\nHigh Scores\n==============="
				for item in high_scores:
					print item
			
	except IOError:
		print "Unable to open file"

def store_high_score(name, score, storage_type):
	"""Store a highscore with player name"""

	try:
		if storage_type is "pickle":
			with open("high-scores.dat", "rb") as f:
				high_scores = pickle.load(f)
		elif storage_type is "plain_txt":
			with open('high-scores.txt', 'r') as f:
				# split read file into native list
				high_scores = f.read().splitlines()

	except IOError:
		high_scores = []

	# add new score, sort, slice
	# I couldn't get nested sequences (commented out here) to  work for both plain text
	# and pickling, since they have to be stored, written to files as strings for the 
	# plain text file challenge, and read again. With pickling, this works fine either way.
	# This is why other storage formats, such as json, are desired for reading/writing
	
	#entry = (score,name)
	#high_scores.append(entry)
	high_scores.append(str(score) + "\t" +  str(name))
	high_scores.sort(reverse=True)
	# keep high score list to top 10
	high_scores = high_scores[0:10]

	# write out the list to the binary file or plain text
	if storage_type is "pickle":
		with open("high-scores.dat", "wb") as f:
			# Dump the scores to the file
			pickle.dump(high_scores, f)
	elif storage_type is "plain_txt":
		# open for read and write
		with open('high-scores.txt', 'w') as f:
			for score in high_scores:
				f.write(str(score) + "\n")

def main():
	trivia_file = open_file("trivia.txt", "r")
	# Set storage type for high_scores and files being read/written to
	storage_type = "plain_txt"
	title = next_line(trivia_file)
	welcome(title)
	score = 0
	# get first block
	category, question, answers, correct, points, explanation = next_block(trivia_file)
	# keep asking questions while category exists in line
	while category:
		# ask a question
		print category
		print question + "Worth: " + str(points) + " points.\n"
		for j in range(4):
			print j + 1, "-", answers[j].rstrip('\n')
		# get answer
		answer = raw_input("\nWhat's your answer?: ")
		# check answer
		if answer == correct:
			print "\nRight!",
			score = score + int(points)
		else:
			print "\nWrong.",
			print explanation
			print "Score:", score, "\n\n"
		# get next block
		category, question, answers, correct, points, explanation = next_block(trivia_file)
	trivia_file.close()
	print "That was the last question!"
	print "Your final score is:", score
	name = raw_input("Enter your name to store your score: ")

	# store the score in the highscores list
	# Use the third argument to indicate desired storage type: plain_txt/pickle
	
	store_high_score(name, score, storage_type)	
	#store_high_score(name, score, "plain_txt")	

	# ask if the user wants to see the high score list
	print "\nCheck the high score list?"
	response = raw_input("Choice (y/n): ")

	if response is "y":
		print_high_scores(storage_type)

main()
raw_input("\n\nPress the enter key to exit.")
