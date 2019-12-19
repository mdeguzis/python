#!/bin/python3

import math
import os
import random
import re
import sys

'''
## // is the floor division operator
# https://stackoverflow.com/questions/14444520/two-forward-slashes-in-python

So, instead of 3/10 being 3.3333333333333335, 3 // 10 is "3".
3 is the "floor" vs. the floating point side.

# Other methods users used:
https://www.hackerrank.com/challenges/repeated-string/forum
'''

# The idea here is to not "repeat the string", but to use math
# to calcuate the repeats.
def repeatedString(s, n):
    # How many a's in string?
    slen = s.count('a')
    # Get the floor and remainder (modulus)
    floor = n // len(s)
    remainder = n % len(s)
    # Multiply original count by "base" floor
    # Add the count of the remainder slice
    count = slen * floor + s[:remainder].count('a')

    return count 

if __name__ == '__main__':
    #s = input()
    s = 'aba'
    #n = int(input())
    n = 10
    result = repeatedString(s, n)
    print(result)

