#!/bin/python

# This program emulates a mood ring

import random

print "\nI can sense your energy bro. Your true emotions are coming across my screen"
print "You are....\n"

mood = random.randint(1,4)

if mood == 1:
    # happy
    print( \
    '''
    -------------
    |           |
    |           |
    |  O     O  |
    |     <     |
    |           |
    | .       . |
    |  .     .  |
    |   .....   |
    -------------
    ''')

elif mood == 2:
    # netral
    print( \
    '''
    -------------
    |           |
    |           |
    |  O     O  |
    |     <     |
    |           |
    | --------- |
    |           |
    |           |
    -------------
    ''')

elif mood == 3:
    # sad
    print( \
    '''
    -------------
    |           |
    |           |
    |  O     O  |
    |     <     |
    |           |
    |    ...    |
    |  .     .  |
    | .       . |
    -------------
    ''')

elif mood == 4:
    # angry
    print( \
    '''
    -------------
    | \       / |
    |  \     /  |
    |   o   o   |
    |     <     |
    |           |
    |  wwwwwww  |
    |           |
    |           |
    -------------
    ''')

else:
    print "Illegal mood value! (You must be in a really good mood)."


