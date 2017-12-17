#!/bin/python2
#
# Description: Teaches object-oriented basics, such as
#			   classes and objects 

# Define a class based on the built in type, object
class Critter(object):
	"""A virtual pet"""

	# Define a method
	def talk(self):
		print "Hi. I'm an instqance of class Critter"

# main
# Instantiate our object
crit = Critter()

# Call the talk method for the crit object
crit.talk()

raw_input("\nPress the enter key to exit.")
