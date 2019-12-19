#!/bin/python

# Description:
# Flips a coin 100 times and reports the total number
# of heads and tails

# Pull in modules
import random

# Initialize vars
heads = 0
tails = 0
coin_flip_count = 0

print \
'''
=================================
Coin flip program
=================================
'''

raw_input("Press enter to continue")
print "\nFlipping all the coins ..."

while coin_flip_count < 100:

    # flip coin
    coin_flip = random.randint(1,2)

    # get heads or tails
    if coin_flip == 1:

        heads += 1

    elif coin_flip == 2:

        tails +=1

    # Enumerate the coin_flip_count
    coin_flip_count += 1

print "Number of heads: " + str(heads)
print "Number of tails: " + str(tails)

