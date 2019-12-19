#!/usr/bin/python

# Birthday wish program
# Demonstrates keyword arguments and default parameter values
# written for python2

# positional parameters
def birthday1(name, age):
		print "Happy birthday,", name, "!", " I hear you're", age, "today.\n"

# parameters with default values
def birthday2(name = "Jackson", age = 1):
		print "Happy birthday,", name, "!", " I hear you're", age, "today.\n"

# The first parameter gets the first value sent, the second parameter 
# gets the second value sent, and so on.
# With this particular function call, it means that name gets "Jackson" and age gets 1
birthday1("Jackson", 1)

# If you switch the positions of two arguments, the parameters get different values. 
# So with the call birthday1 name gets the first value, 1 , and age gets 
# the second value, "Jackson"
birthday1(1, "Jackson")

# Positional parameters get values sent to them in order, unless you tell the 
# function otherwise (seen below). Both are valid, since we are giving the values
# by name.
birthday1(name = "Jackson", age = 1)
birthday1(age = 1, name = "Jackson")

# This set of functions demonstrates giving default values
# The first uses name=Jackson, age=1, since the function defines those defaults
# In the second, the name is given, so the default name is not used.
# Same logic goes for the rest.
birthday2()
birthday2(name = "Katherine")
birthday2(age = 12)
birthday2(name = "Katherine", age = 12)
birthday2("Katherine", 12)

raw_input("\n\nPress the enter key to exit.")
