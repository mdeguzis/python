#!/usr/bin/python

# Word jumpble

# The computer picks a random word and then "jumbles" it
# The player has to guess the original word
# Written for python 2

import random

# Create the constant for the jumpble
WORDS = ("python", "jumble", "easy", "difficult", "answer", "xylophone")

# use random.choice() to pull randomly from a sequence
word = random.choice(WORDS)

# create a variable to use later to see if the guess is correct
correct = word

# create the jumbled version of the word
jumble = ""

# loop until word is equal to the emptry string above
# each time the loop executes, the computer creates a new version of 'word'
# with one letter extracted and assigns it back to word. Eventually, 'word'
# will become the empty string and the jumbling will be done.

while word:
	# get random pos in 'word'
	position = random.randrange(len(word))

	# create the new version of the string 'jumble'
	jumble += word[position]

	# create new versio of word
	# Using slicing, we create two new strings from 'word'
	# The first, 'word[:position]', is every letter up to, but no including 'word[position]'
	# the next, 'word[position]' 
	word = word[:position] + word[(position + 1):]

# Welcome screen for player

print \
"""
	Weclome to word jumble!

   Unscramble the letters to make a word
(Press the ENTER key at the prompt to quit)

"""

print "The jumble is:", jumble

# Start guess process
guess = raw_input("Your guess: ")

while guess != correct and guess != "":
	print "Sorry, that's not it."
	guess = raw_input("\nYour guess: ")

# This check is outside the while loop since the user could guess
# right on the first try and skip the loop entirely
if guess == correct:
	print "That's it! You guessed it!"

print "Thanks for playing\n"

