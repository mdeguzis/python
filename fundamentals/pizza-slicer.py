#!/usr/bin/python

# Pizza Slice program
# Demonstrates string slicing
# written for python2

# import 'print()' from python 3 to make this work with python2
from __future__ import print_function

word = "pizza"

print(
"""
 Slicing 'cheat sheet'

 0   1   2   3   4   5
 +---+---+---+---+---+
 | p | i | z | z | a |
 +---+---+---+---+---+

-5  -4  -3  -2  -1
"""
)

print("Enter the beginning and ending index for your slice of 'pizza'.")
print("Press the ENTER key at 'Start' to exit.")

# 'None' is a special way of representing nothing, akin to 'NULL'
# The purpose here is to initialize 'start'
# It is a good placeholder for a value
# It will also evauluate to False.
start = None

# loop while start is not blank
# if input is entered, proceed to if conditional and ask for 'finish'
# ensure values are int
# This will then print the index requested
# in comparison to indexing, slicing takes a start/end, vs. indexing being singular

while start != "":

	start = raw_input("Start: ")

	if start:
		start = int(start)
		finish = int(raw_input("Finish: "))		

		print("word[", start, ":", finish, "] is ", end= " ")
		print(word[start:finish])

# Note:
# There is also a shorthand for slicing
# Given the word being 'pizza', you can issue:
# 	print word[0:4]
# to get "pizz"
