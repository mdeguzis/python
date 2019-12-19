#!/bin/python

# Random access program
# Demonstates string indexing

import random

word = "index"
print "The word is: ", word, "\n"

# get the positive and negative length of the word
high = len(word)
low = -len(word)

# What we are doing here is iterating though a range of 10
# and pulling a random range of word. 
# You can check against values yourself by issuing 'print word[0]'
# or whatever index you wish.

for i in range(10):
    position = random.randrange(low,high)
    print "word[", position, "]\t", word[position]

print "\nCompare the above random index to the below manual index"
print "Remember that negative indexes walk backwards\n"

# this makes use of enumerate to "walk" the index
for x, y in enumerate(word):
    print "word[",x,"]\t", y
