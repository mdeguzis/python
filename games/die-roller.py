#!/bin/python

import random

# Generate the die rolls

# Syntax: randint(<start_range>,<end_range>)
# Syntax: randrange(<integer_range>)
 
# random - the module
# randint - the function "randint" from the module "random"
# randint() - produce a random integer
# This method of access is called "dot notation"

# There are many ways of using randrange(), but a simplist is a using postitive integer
# In the below example, a range of 6 would start start with 0 and end with 5.
# Add + 1 to the range so we end up with the correct result
# Use of either function accomplishes the same thing

die1 = random.randint(1,6)
die2 = random.randrange(6) + 1

# add them up
total = die1 + die2

print "You rolled:", die1, "and a", die2, "for a toal of: ", total
