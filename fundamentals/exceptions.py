#!/bin/python

# get an exception's argument
# Written for python2

try:
	num = float(raw_input("\nEnter a number: "))

except ValueError as e:
	print("That was not a number! Or as Python would say...")
	print(e)
else:
	print("You entered a number")
