#!/usr/bin/python

# Handle It
# Demonstrates handling exceptions
# try/except
# written for python2

# allow future functions for print
from __future__ import print_function

try:
	num = float(raw_input("Enter a number: "))
except:
	print("Something went wrong!")

# specifying exception type
try:
	num = float(raw_input("\nEnter a number: "))
except ValueError:
	print("That was not a number!")

# handle multiple exception types
# This code tries to convert two different values to a floating-point number.
# Both fail, but each raises a different exception type
# Float only accepts strings and numbers, none None
# "Hi!" raises an error as the chars are of the wrong value, not digits

print()
for value in (None, "Hi!"):
	try:
		print("Attempting to convert", value, "-->", end=" ")
		print(float(value))
	except (TypeError, ValueError):
		print("Something went wrong!")

# using multiple except clauses
print()
for value in (None, "Hi!"):
	try:
		print("Attempting to convert", value, "-->", end=" ")
		print(float(value))
	except TypeError:
		print("I can only convert a string or a number!")
	except ValueError:
		print("I can only convert a string of digits!")


# get an exception's argument
try:
	num = float(input("\nEnter a number: "))
except ValueError as e:
	print("That was not a number! Or as Python would say...")
	print(e)

# try/except/else
# Think of the else here as "passing" through exception catches and
# sucessfully showing the output of "try"
try:
	num = float(raw_input("\nEnter a number: "))
except ValueError:
	print("That was not a number!")
else:
	print("You entered the number", num)
	raw_input("\n\nPress the enter key to exit.")
