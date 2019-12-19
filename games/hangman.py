#!/usr/bin/python

# The classic game of Hangman. The computer picks a random word
# and the player wrong to guess it, one letter at a time. If the player
# can't guess the word in time, the little stick figure gets hanged.
# Written in python 2

import random

# Now will be a long sequence of 8 tupes. It is mostly ascii art

# constants
HANGMAN = (
"""
------
|    |
|
|
|
|
|
|
|
----------
""",
"""
------
|    |
|    O
|
|
|
|
|
|
----------
""",
"""
------
|    |
|    O
|   -+-
|
|
|
|
|
----------
""",
"""
------
|    |
|    O
|  /-+-
|
|
|
|
|
----------
""",
"""
------
|    |
|    O
|  /-+-/
|
|
|
|
|
----------
""",
"""
------
|    |
|    O
|  /-+-/
|    |
|
|
|
|
----------
""",
"""
------
|    |
|    O
|  /-+-/
|    |
|    |
|    |
|    |
|
----------
""",
"""
------
|    |
|    O
|  /-+-/
|    |
|    |
|   | |
|   | |
|
----------
""")

# Max wrong guesses
# This is based on the length of the tuple above
# Subtract one since the first tuple "image" is the starting image.
MAX_WRONG = len(HANGMAN) - 1

WORDS = ("OVERUSED", "LINUX", "ALL YOUR BASE ARE BELONG TO US", "PROGRAMMING", "PYTHON")

# Initialize the variables and choose a random word from the list
word = random.choice(WORDS)

# Create a string to represent what the player has guessed so far
# One dash for each letter in word to be guessed
so_far = "-" * len(word)

# create a variable to count the wrong guesses. Init at 0
wrong = 0

# create an empty list, 'used', to contain all the letters the player guessed
used = []


