#!/bin/python

# Description: Takes a message from the user and printe it,
# minus any vowels, by creating a new string from the old.
# This is written in python 2

message = raw_input("\nEnter a message: ")
new_message = ""
VOWELS = "aeiou"

print ""

# Walk the message and if the element (variable 'letter') is in the message,
# check if the lowercase version is not in the set of 'VOWELS'
# If it is not, add it to 'new_message'
# the 'VOWELS' are assigned in lowercase, so ensure the message is checked
# in the same case

for letter in message:
    if letter.lower() not in VOWELS:
	new_message += letter
	print "A new string has been created:" + new_message

print "Your message without vowels is: " + new_message + "\n"
