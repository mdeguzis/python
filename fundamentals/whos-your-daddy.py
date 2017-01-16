#!/usr/bin/python

# Who's your daddy program
# Demonstrates using dictionaries
# Written for python 2

# create the dictionary
# each item is made up of a key and a value

family = {"Michael DeGuzis" : "Thomas DeGuzis Jr.",
"Layla DeGuzis" : "Michael DeGuzis",
"Thomas DeGuzis Jr." : "Thomas DeGuzis Sr.",
"Thomas DeGuzis Sr." : "Father to Tom DeGuzis Jr."}

# Menu

choice = None
while choice != "0":
	print  \
	"""
	Who's your daddy program
	================================
	0 - Quit
	1 - Look Up a family member
	2 - Get a family member's grandfather
	3 - Add a family member pair
	4 - Replace a family member pair
	5 - Delete a family member pair
	6 - Show all items
	"""

	choice = raw_input("Choice: ")
	print ""

	# exit
	if choice == "0":
		print "Goodbye."

	# get a family_member
	# Get the value from the family_member "key"
	elif choice == "1":
		family_member = raw_input("Which family member should I look up?: ")
		if family_member in family:
			# This assigns the value from family, where key is "family_member", and assigns it to "father"
			# Remember, dictionaries are accessed commonly via "dictionary[key]", which returns the key's value
			father = family[family_member]
			print "\n", family_member + "'s dad is " + father
		else:
			print "\nSorry, I don't know " + family_member

	# Get family member's grandfather
	elif choice == "2":
		family_member = raw_input("Which family mamber should I check a grandfather for?: ")
		if family_member in family:
			# This assigns the value from family, where key is "family_member", and assigns it to "father"
			father = family[family_member]
			# This goes further, checking the "father" value as an actual key request in family. Assin the
			# returned value as the grandfather
			if father in family:
				grandfather = family[father]
			print "\n", family_member + "'s grandfather is " + grandfather
		else:
			print "\nSorry, I don't know " + family_member


	# add a family_member-family_member pair
	# Note: If you assign a value to a dictionary using a key that already 
	# exists, Python replaces the current value without complaint.
	elif choice == "3":
		family_member = raw_input("Who do you want me to add?: ")
		if family_member not in family:
			family_member = raw_input("\nWho is their father?: ")
			family[family_member] = family_member
			print "\n", family_member + " has been added."
		else:
			print "\nThat family_member already exists! Try changing it."

	# redefine an existing term
	elif choice == "4":
		term = raw_input("What family member pair do you want me to redefine?: ")
		if family_member in family:
			family_member = raw_input("What's the new definition?: ")
			family[family_member] = family_member
			print "\n", family_member + " has been redefined."
		else:
			print "\nThat family member pair doesn't exist! Try adding it."

	# delete a family_member-family_member pair
	elif choice == "5":
		family_member = raw_input("What family member do you want me to delete?: ")
		if family_member in family:
			del family[family_member]
			print "\nOkay, I deleted " + family_member
		else:
			print "\nI can't do that! "+ family_member, "doesn't exist in the family tree."

	elif choice == "6":
		print "\nHere are all the items in the family tree:\n"
		print family.items()

	# some unknown choice
	else:
		print "\nSorry, but", choice, "isn't a valid choice."
		raw_input("\n\nPress the enter key to exit.")
