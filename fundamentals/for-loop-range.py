#!/bin/python

# Counter
# Demonstrates the range() function

# NOTE:
# The 'end=""' portion of the print function is python 3
# To make this work in python 2, uncomment the below:
# If using python 3, raw_input must be input()

from __future__ import print_function

print("\nCounting:")

# range() returns a sequence of numbers on screen, but what
# it is actually doing, is just returning the next number in
# sequence, one by one.

# syntax: range(<start>, <end>, <stepping>)
# the syntax only needs an end range, meaning:
# range(10), tells the function to count 0 10
# <stepping> just 
for i in range(10):
    print (i, end=" ")

print("\nCounting by fives:")

for i in range(0, 50, 5):
    print (i, end=" ")

print ("\nCounting backwards:")

for i in range(10, 0, -1):
    print (i, end=" ")
   
raw_input("\n\nPress enter to exit.\n")
