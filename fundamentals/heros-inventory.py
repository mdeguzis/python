#!/usr/bin/python

# Hero's inventory
# Demonstrates tuple creation
# Written for python2

# Create an empty tuple
inventory = ()

# treat the tuple as a condition
if not inventory:
	print "You are empty-handed"

raw_input("Press the enter key to continue")

# create a tuple with some items
inventory = ("sword", 
	    "armor",
            "shield",
            "healing potion")

# print the tuple
print "\nThe tuple inventory is: "
print inventory

# Print each element in the tuple
print "\nYour items: "

for item in inventory:
	print item


		
