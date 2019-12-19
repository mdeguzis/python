#!/usr/bin/python

# Hero's Inventory v3.0
# Demonstrates lists instead of tuples
# Written for python2

# import 'print()' from python 3 to make this work with python2
from __future__ import print_function

# Create an empty tuple
inventory = []

# treat the tuple as a condition
if not inventory:
	print("You are empty-handed")

raw_input("Press the enter key to continue")

# create a tuple with some items
inventory = ["sword", 
	    "armor",
            "shield",
            "healing potion"]

# print the tuple
print("\nThe tuple inventory is: ")
print(inventory)

# Print each element in the tuple
print("\nYour items: ")

for item in inventory:
	print(item)

# Now use len() to count the items
print("\nYou have", len(inventory), "items in your inventory")

# Demonstrate using an operator
if "healing potion" in inventory:
	print("You will live to fight another day.")

# display one item through an index
index = int(raw_input("Enter the item number from the inventory: "))
print("At index", index, "is the item", inventory[index])

# Slicing tuples

print(
"""
 Slicing 'cheat sheet'
  0       1        2        3                4
  +-------+--------+--------+----------------+
  | sword | armour | shield | healing potion |
  +-------+--------+--------+----------------+
  -4     -3       -2       -1 
""")

start = int(raw_input("Enter the index number to begin the slice: "))
finish = int(raw_input("Enter the index number to end the slice: "))
print("Inventory[", start, ":", finish, "] is", end= " ")
print(inventory[start:finish])

# Concatenating tuples
chest = ["gold", "gems"]
print("\nyou find a chest. It contains:")
print(chest)
print("You add these to your inventory.")
inventory += chest

# show new inventory
print("You inventory is now:")
print(inventory)

# demonstrate assigning a new list element by index
# this shows how lists are mutable (changable).

print("\nYou change your sword for a crossbow.")
inventory[0] = "crossbow"
print("Your inventory is now:")
print(inventory)

# assign by slice
print("\nYou use your gold and gems to buy an orb of future tellling.")
inventory[4:6] = ["orb of future telling"]
print("Your inventory is now:")
print(inventory)

# deleting a list element
print("\nIn a great battle, you shield is destroyed")
del inventory[2]
print("Your inventory is now:")
print(inventory)

# delete a list slice
print("\nYour crossbow and armor are stolen by thieves!")
del inventory[0:2]
print("Your inventory is now:")
print(inventory)
