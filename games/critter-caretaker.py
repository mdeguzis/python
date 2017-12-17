#!/bin/python2
#
# Description: Teaches object-oriented basics, such as
#			   classes, objects, attributes, and more

# Define a class based on the built in type, object
class Critter(object):
	"""A virtual pet"""

	# Define a basic total attribute
	total = 0

	# Define a static class attribute for tracking critter totals
	@staticmethod
	def status():
		print "\nThe total number of critters is", Critter.total

	# Define a contructor
	def __init__(self, name):
		print "A new critter has been born."
		# Create the attribute "name"
		self.name = name
		# Update the critter total for the static class attribute above
		Critter.total += 1

	# Define an attribute string representation
	# Normally, printing an object outputs something like:
	#	 <__main__.Critter object at 0x00A0BA90>
	def __str__(self):
		rep = "Critter object\n"
		rep += "name: " + self.name + "\n"
		return rep

	def talk(self):
		print "Hi. I'm", self.name, "\n"

	# Define a method
	def talk(self):
		# Output using the previously defined name attribute
		print "Hi. I'm " + self.name

# main
# Instantiate our object
#crit1 = Critter()
#crit2 = Critter()

# This line invokes the talk() method of the Critter object assigned to crit
#crit1.talk()
#crit2.talk()

# Output attributes. 
# In this block of code, a parameter is passed to the Critter class
#crit1 = Critter("Poochie")
#crit1.talk()
#crit2 = Critter("Randolph")
#crit2.talk()

#print "\nPrinting crit1:"
#print crit1
#print "Directly accessing crit1.name"
#print crit1.name

print "Accessing the class attribute Critter.total:"
print Critter.total

print "\nCreating critters..."
crit1 = Critter("critter 1")
crit2 = Critter("critter 2")
crit3 = Critter("critter 3")

# Call the status method
Critter.status()

print "Accessing the class attribute through an object (crit1): "
print crit1.total

raw_input("\nPress the enter key to exit.")
